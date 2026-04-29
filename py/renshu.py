color=[0,1,2,0]
adj=[
    [0,1,1,0],
    [1,0,0,0],
    [1,0,0,0],
    [0,0,0,0]
]

v=0

used=[0]*5

for u in range(4):
    if adj[v][u] ==1 and color[u]!=0:
        used[color[u]]=1

print(used)
