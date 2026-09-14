-- I come back here over a year later to document more stupidity
print(#tostring(-0))
print(#tostring(0))
-- You'd probably expect 2 and 1, but nope, it isn't (and differs per version)
-- on Lua 5.1 you get "2 2" (if the first zero constant seen is negative zero, all zeros become negative zero, and vice versa)
-- yes, this means if you swap the order, you start getting "1 1" on Lua 5.1
-- on Lua 5.4 you get "1 1" (negative zero seems to just not be supported at all)
-- on Luau you get "2 1" (it actually correctly differs between -0 and 0)
