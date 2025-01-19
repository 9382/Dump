-- Turns out there's a bug in lua versions 5.1 to 5.2.2 to do with functions with lots of parameters
-- The stack wouldn't be correctly sized and the program would likely crash soon after running the function
-- Turns out this is a known CVE, specifically CVE-2014-5461, and since I was using regular lua 5.1.5 source, I didn't have the patch
-- The below is a pretty simple way to test if you have a broken version. If any of the prints below do not show, you are vulnerable

print(1)
pcall(function(_, a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, ...)
        print(2)
        a(b, c(...))
end)
print(3)
