\ENCODING=ISO-8859-1
\Problem name: 

Maximize
 obj: y000f + y000t + y010f + y010t
Subject To
 c1:  x00f <= 1.1
 c2:  x00t <= 1.1
 c3:  x01f <= 2.3
 c4:  x01t <= 2.3
 c5:  - x00t + b00 <= 0
 c6:  x00t - 1.1 b00 <= 0
 c7:  - x00f + x00t + 7.2 b00 <= 10.8
 c8:  x00t - x01f + 3.6 b00 + 3.6 b01 <= 12.1
 c9:  - x01t + b01 <= 0
 c10: x01t - 2.3 b01 <= 0
 c11: - x00f + x01t + 3.6 b00 + 3.6 b01 <= 9.5
 c12: - x01f + x01t + 7.2 b01 <= 10.8
 c13: x00f - x00t <= 0
 c14: x01f - x01t <= 0
 c15: y000f + x00f <= 0
 c16: y000t - x00t <= 0
 c17: y010f + x01f <= 0
 c18: y010t - x01t <= 0
Bounds
 -Inf <= y000f <= 0
 -Inf <= y010f <= 0
 0 <= b00 <= 1
 0 <= b01 <= 1
Binaries
 b00  b01 
End
