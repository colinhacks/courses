using JuMP
using Gurobi
include("modules.jl")


###########################
####  INITIALIZATION   ####
###########################

# large images or small?
large = true
# Reads in two training files
# 'fours.csv' contains images that are not sixes
# 'sixes.csv' contains images that are sixes
# x=readcsv("dataset/train_4s_10x10.csv")
# y=readcsv("dataset/train_6s_10x10.csv")
if large
    x = readcsv("dataset/train_4s_10x10.csv")
    y = readcsv("dataset/train_6s_10x10.csv")
else
    x = readcsv("train_fours.csv")
    y = readcsv("train_sixes.csv")
end

# MODEL PARAMETERS
H=3                 # H is the number of nodes in the hidden layer
P=size(x, 2)        # P is the number of pixels
M=P+2               # Big M 
ep=.001             # epsilon


# Training parameters
# Minibatch sampling rate
p_sample = .2        # Sampling rate for minibatch generation 
p_dropout = .5       # Dropout sampling rate
init = "zero"       # Initialization technique: {"rand", "zero"}
numiter = 20        # Number of iterations
time_limit = 120      # Time limit per iteration (seconds)
mip_gap = .05     # MIP Gap: the relative gap between the lower and upper objective bound is less than MIPGap times the upper bound
sp = 0              # Sparsity penalty
disc_const = .5            # Discount rate
disc_var = .5            # Discount rate
wdp_const = 0
wdp_var = 6

#####################
####  TRAINING   ####
#####################

# Weight initialization
if init=="rand"      # discretize imported from modules.jl
    tw = rand(H,P)
    tv = rand(H)
    tw = map(discretize,tw)
    tv = map(discretize,tv)
elseif init=="zero"
    tw = zeros(H,P)
    tv = zeros(H)
end
println("Initialized weights")


xresults = []
yresults = []
xnum = []
xcor = []
ynum = []
ycor = []
succ = []
opos = []
oneg = []
wdiff = []
vdiff = []
objs = []
sizeX = 0
sizeY = 0

for iteration in 1:numiter

    # tw = zeros(H,P)
    # tv = zeros(H)    

    wdp = wdp_const + wdp_var*iteration/(P*H)
    disc = (numiter-iteration)/numiter

    #######################
    #### GEN MINIBATCH ####
    #######################
    
    # Minibatch sampling
    modx = minibatch(x,p_sample)
    mody = minibatch(y,p_sample)
    println(size(modx))
    println(size(mody))
    data=[modx;mody]

    # N is the number of training images
    N = size(data,1)
    npos = size(modx,1) 
    nneg = size(mody,1)

    xnum = [xnum;npos]
    ynum = [ynum;nneg]

    
    ######################
    #### DEFINE MODEL ####
    ######################

    m = Model(solver=GurobiSolver(MIPGap=mip_gap, TimeLimit=time_limit))

    # Input-to-Hidden layer weights (Integers from -1 to 1)
    @defVar(m, -1 <= w[1:H,1:P] <= 1, Int)
    # Hidden-to-Output layer weights (Integers from -1 to 1)
    @defVar(m, -1 <= v[1:H] <= 1, Int)
    # Hidden layer binary outputs
    @defVar(m, hv[1:N,1:H], Bin)
    # Output layer binary outputs
    @defVar(m, o[1:N], Bin)
    # Dummy variables for the absolute value in the objective function
    @defVar(m, dw[1:H,1:P])
    @defVar(m, dv[1:H])
    # @defVar(m, aw[1:H,1:P])
    # @defVar(m, av[1:H])


    # Limits hidden variables to be 1 if the dot product of the input vector and the input-to-hidden
    # weights, and 0 otherwise. 
    for n in 1:N
        for h in 1:H
            @addConstraint(m,sum(data[n,1:P].*w[h,1:P]) >= ep - M * (1-hv[n,h]))
        end
    end

    for n in 1:N
        for h in 1:H
            @addConstraint(m,sum(data[n,1:P].*w[h,1:P]) <= ep + M *hv[n,h])
        end
    end

    # # Limits output variables to be 1 if the dot product of the hidden layer's outputs and the hidden-to-output
    # # weights, and 0 otherwise. 
    #hv[n,1]*v[1] + hv[n,2]*v[2] + hv[n,3]*v[3]+ hv[n,4]*v[4]+ hv[n,5]*v[5]+ hv[n,6]*v[6]+ hv[n,7]*v[7]+ hv[n,8]*v[8]+ hv[n,9]*v[9]+ hv[n,10]*v[10]
    for n in 1:N
        @addConstraint(m, dot(vec(hv[n,:]),v) + M*(1-o[n])>= ep)
    end

    for n in 1:N
        @addConstraint(m, dot(vec(hv[n,:]),v) - M*o[n] <= ep)
    end

    # DROPOUT
    for h in 1:H
        for p in 1:P
            if rand()<p_dropout
                @addConstraint(m, w[h,p]==0)
            end
        end
    end

    # Because we maintain an exogenous set of weights that we update iteratively, we don't want
    # the weights to be completel overwritten each time we run an iteration
    # Thus we put a term i nthe objective that tries to minimize the absolute value of changes to 
    # the network's weights. Having an absolute value in the objective requires a set of constraints
    # to be added
    for h in 1:H
        for p in 1:P
            @addConstraint(m, -1.0*dw[h,p]<=w[h,p]-tw[h,p])
            @addConstraint(m, w[h,p]-tw[h,p]<=dw[h,p])
        end
    end
    for h in 1:H
        @addConstraint(m, -1.0*dv[h]<=v[h]-tv[h])
        @addConstraint(m,v[h]-tv[h]<=dv[h])
    end



    # for h in 1:H
    #     for p in 1:P
    #         @addConstraint(m, -1.0*aw[h,p]<=w[h,p])
    #         @addConstraint(m, w[h,p]<=aw[h,p])
    #     end
    # end
    # for h in 1:H
    #     @addConstraint(m, -1.0*av[h]<=v[h])
    #     @addConstraint(m,v[h]<=av[h])
    # end


    # Objective function minimizes number of incorrect identifications
    # as well as the changes made to the exogenous weights tw and tv
    @setObjective(m, Min, sum(o[1:npos]) - sum(o[npos+1:N]) + wdp*(sum(dw) + sum(dv)))

    # Solve model
    status = solve(m)

    # Reassignment
    # Print weight results 
    foundw = getValue(w)
    foundv = getValue(v)
    tw = (1-disc)*tw + disc*foundw
    tv = (1-disc)*tv + disc*foundv


    ##################
    #### PRINTING ####
    ##################

    
    founddw = getValue(dw)
    founddv = getValue(dv)
    foundo = getValue(o)
    
    xrate = npos-sum(foundo[1:npos])
    xcor = [xcor;xrate]
    yrate = sum(foundo[npos+1:N])
    ycor = [ycor;yrate]
    succ = [succ;(xrate+yrate)/(npos+nneg)]
    

    ####################
    ####  TESTING   ####
    ####################

    # Testing Data:
    if large
        test_x = readcsv("dataset/test_4s_10x10.csv")
        test_y = readcsv("dataset/test_6s_10x10.csv")
    else
        test_x = readcsv("test_fours.csv")
        test_y = readcsv("test_sixes.csv")
    end

    println("Calc sizeX: ",size(test_x,1))
    sizeX = size(test_x,1)
    sizeY = size(test_y,1)

    numCorrect = 0
    for n in 1:sizeX
        total = 0
        for h in 1:H
            hidden_value = sum(test_x[n,1:P].*tw[h,1:P])#getValue(sum(test_x[n,1:P].*tw[h,1:P]))
            if hidden_value > 0
                total = total + tv[h]#getValue(tv[h])
            end
        end
        if total <= 0
            numCorrect = numCorrect + 1
        end
    end

    println("Minibatch Information:")
    println("# positive examples: ",size(modx,1))
    println("# negative examples: ",size(mody,1))

    println("Results of Testing Data: ")
    println("Number of non-sixes correctly rejected out of ", sizeX, ": ", numCorrect)
    xresult = numCorrect
    xresults = [xresults;xresult]
    

    numCorrect = 0
    for n in 1:sizeY
        total = 0
        for h in 1:H
            hidden_value = sum(test_y[n,1:P].*tw[h,1:P])#getValue(sum(test_y[n,1:P].*tw[h,1:P]))
            if hidden_value > 0
                total = total + tv[h]#getValue(tv[h])
            end
        end
        if total > 0
            numCorrect = numCorrect + 1
        end
    end
    println("Number of sixes correctly recognized out of ", sizeY, ": ", numCorrect)
    yresult = numCorrect
    yresults = [yresults;yresult]

    
    opos = [opos;sum(getValue(o)[1:npos])]
    oneg = [oneg;-1*sum(getValue(o)[npos+1:N])]
    
    println("wdiff")
    println(wdp*sum(founddw))
    println("vdiff")
    println(wdp*sum(founddv))
    wdiff = [wdiff;wdp*sum(founddw)]
    vdiff = [vdiff;wdp*sum(founddv)]
    obj = getObjectiveValue(m)
    objs = [objs;obj]


    println("TRAINING")
    println(string("train x: ", xrate, "/", npos, "=", xrate/npos))
    println(string("train y: ", yrate, "/", nneg, "=", yrate/nneg))
    println(string("for a success rate of: ",succ))
    println("\nDIFF")
    println(string("w diff: ", sum(founddw),"*",wdp,"=",wdp*sum(founddw)))
    println(string("v diff: ", sum(founddv),"*",wdp,"=",wdp*sum(founddv)))
    println(string("Objective value: ", obj)) 
    println(string("\nTESTING"))
    println(string("test x: ", xresult, "/", size(test_x,1))) 
    println(string("test y: ", yresult, "/",size(test_y,1)))      
    println(string("for a success rate of: ", (xresult+yresult)/(sizeX+sizeY)))

end



#results = ["xresults" "yresults" "xnum" "xcor" "ynum" "ycor" "succ" "wdiff" "vdiff" "objs"]
println("\n\n\n#############################\n###    RESULTS OVERVIEW   ###\n#############################")
println([fill("train x: ",numiter) xcor     fill("/",numiter) xnum fill(" train y: ",numiter) ycor      fill("/",numiter)     ynum fill(" for a success rate of: ",numiter) succ])
println([fill("w diff: ",numiter) wdiff fill("v diff: ",numiter) vdiff])
println([fill("Objective values: ",numiter) objs]) 
println()
println([fill("test x: ",numiter)  xresults  fill(" |   test y: ",numiter)   yresults    fill(" |   success rate: ",numiter) (xresults+yresults)/(sizeX+sizeY) ])




