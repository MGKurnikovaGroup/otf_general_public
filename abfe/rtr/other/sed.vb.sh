#!/bin/bash

# lambda = 0.00
sed 's/=1\.000000/=0.0000/g' k.RST > k-la-0.00.RST
sed -i 's/=5\.000000/=0.0000/g' k-la-0.00.RST
sed -i 's/=10\.000000/=0.0000/g' k-la-0.00.RST

# lambda = 0.05
sed 's/=1\.000000/=0.0500/g' k.RST > k-la-0.05.RST
sed -i 's/=5\.000000/=0.2500/g' k-la-0.05.RST
sed -i 's/=10\.000000/=0.5000/g' k-la-0.05.RST

# lambda = 0.10
sed 's/=1\.000000/=0.100/g' k.RST > k-la-0.10.RST
sed -i 's/=5\.000000/=0.5000/g' k-la-0.10.RST
sed -i 's/=10\.000000/=1.0000/g' k-la-0.10.RST

# lambda = 0.20
sed 's/=1\.000000/=0.2000/g' k.RST > k-la-0.20.RST
sed -i 's/=5\.000000/=1.0000/g' k-la-0.20.RST
sed -i 's/=10\.000000/=2.0000/g' k-la-0.20.RST

# lambda = 0.30
sed 's/=1\.000000/=0.3000/g' k.RST > k-la-0.30.RST
sed -i 's/=5\.000000/=1.5000/g' k-la-0.30.RST
sed -i 's/=10\.000000/=3.0000/g' k-la-0.30.RST

# lambda = 0.50
sed 's/=1\.000000/=0.5000/g' k.RST > k-la-0.50.RST
sed -i 's/=5\.000000/=2.5000/g' k-la-0.50.RST
sed -i 's/=10\.000000/=5.0000/g' k-la-0.50.RST

