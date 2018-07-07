\ENCODING=ISO-8859-1
\Problem name: 

Maximize
 obj: y000f + y000t + y001f + y001t - y100f - y100t
Subject To
 c1:  x00f <= 2
 c2:  x00t <= 2
 c3:  x10f <= 2
 c4:  x10t <= 2
 c5:  - x00t + b00 <= 0
 c6:  x00t - 2 b00 <= 0
 c7:  - x00f + x00t + 4 b00 <= 5
 c8:  - x10t + b10 <= 0
 c9:  x10t - 2 b10 <= 0
 c10: - x10f + x10t + 4 b10 <= 5
 c11: x00f - x00t <= 0
 c12: x10f - x10t <= 0
 c13: y000f + x00f <= 0
 c14: y000t - x00t <= 0
 c15: y001f + x10f <= 0
 c16: y001t - x10t <= 0
 c17: y100f + x00f <= 0
 c18: y100t - x00t <= 0
 c19: y100f + x10f <= 0
 c20: y100t - x10t <= 0
Bounds
 -Inf <= y000f <= 0
 -Inf <= y001f <= 0
 -Inf <= y100f <= 0
 0 <= b00 <= 1
 0 <= b10 <= 1
Binaries
 b00  b10 
End
