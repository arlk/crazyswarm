using YAML
using BayesianOptimization, GaussianProcesses
import ControlSystems: tf, c2d, ss

function cflie(x)
    x[1] *= 100
    x[2] *= 100
    x[3] *= 1000
    x[4] *= 1000
    println("\n\n\nωᵥ = $(x[1]),  ωw = $(x[2]), Am_v = $(x[3]), Am_w = $(x[4])\n")
    ssv = ss(c2d(tf(x[1],[1, x[1]]), 1/500))
    ssw = ss(c2d(tf(x[2],[1, x[2]]), 1/500))
    println("f_Av = $(ssv.A[1]), f_Cv = $(4*ssv.C[1])\n")
    println("f_Aw = $(ssw.A[1]), f_Cw = $(4*ssw.C[1])\n")
    # csv
    params = Dict("Am_v" => x[3], "Am_w" => x[4],
             "A_v" => ssv.A[1], "C_v" => 4*ssv.C[1],
             "A_w" => ssw.A[1], "C_w" => 4*ssw.C[1],)
    YAML.write_file("log.yaml", params)

    println("Specify the cost:")
    cost = parse(Float64, readline())
    @show typeof(cost)
    return cost
end

model = ElasticGPE(4)
opt = BOpt(cflie, model, UpperConfidenceBound(), MAPGPOptimizer(),
           [0.2, 0.2, -1., -1.], [0.5, 0.5, -0.5, -0.3],
           maxiterations = 20, sense = Min)

result = boptimize!(opt)
