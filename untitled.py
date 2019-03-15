from shape import *

s1 = Rectangle(V(75,75),width = 50, height=50);
s2 = Rectangle(V(120,120),width=20,height=20);
print(check_xy_overlap(s1,s2))