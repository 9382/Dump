print(#{nil, 1} == #{nil, 1, nil}) -- #{nil, 1, nil} is 0... for some reason
print(#{nil, 1} == #{nil, 1, nil, nil})

print(#{nil, 1}, #{nil, 1} == 2) -- This has a length of 2
local t1 = {}; t1[1] = nil; t1[2] = 1
print(#t1, #t1 == 2) -- This has a length of 0 (identical data)
local t2 = {nil, nil}; t2[2] = 1
print(#t2, #t2 == 2) -- This has a length of 2 (same as above yet we started with nil)
