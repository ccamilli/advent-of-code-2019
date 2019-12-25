min_inp = 109165
max_inp = 576723

counts = 0

for i in range(1, 6):
    for j in range(10):
        for k in range(10):
            for l in range(10):
                for m in range(10):
                    for n in range(10):
                        c = 100000*i + 10000*j + 1000*k + 100*l + 10*m + n
                        if (c > min_inp) and (c < max_inp):
                            if (i==j or j==k or k==l or l==m or m==n):
                                if (i<=j and j<=k and k<=l and l<=m and m<=n):
                                    counts += 1
                                    
ans1 = counts
print("Answer for part 1 is", ans1)

counts = 0
for i in range(1, 6):
    for j in range(10):
        for k in range(10):
            for l in range(10):
                for m in range(10):
                    for n in range(10):
                        c = 100000*i + 10000*j + 1000*k + 100*l + 10*m + n
                        if (c > min_inp) and (c < max_inp):
                            if ((i==j and j!=k) or (j==k and i!=j and k!=l) or
                                (k==l and j!=k and l!=m) or (l==m and l!=k and m!=n)
                                or (m==n and m!=l)):
                                if (i<=j and j<=k and k<=l and l<=m and m<=n):
                                    counts += 1
ans2 = counts
print("Answer for part 2 is", ans2)