import os, math, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
os.makedirs("assets", exist_ok=True)
INK="#1f2933"; GRID="#d9dee3"; BLUE="#2563eb"; ORANGE="#e8702a"; GREEN="#2f9e44"; GREY="#8a949e"; RED="#c92a2a"
plt.rcParams.update({"font.size":11,"axes.edgecolor":INK,"axes.labelcolor":INK,"xtick.color":INK,"ytick.color":INK,
 "text.color":INK,"axes.spines.top":False,"axes.spines.right":False,"axes.grid":True,"grid.color":GRID,"grid.linewidth":0.8,
 "figure.facecolor":"white","axes.facecolor":"white","svg.fonttype":"path","axes.titleweight":"bold","axes.titlesize":13})
PREVIEW=os.environ.get("PREVIEW")
def save(fig,name):
    fig.savefig(f"assets/{name}.svg",bbox_inches="tight",facecolor="white")
    if PREVIEW: fig.savefig(f"/tmp/cl_{name}.png",bbox_inches="tight",facecolor="white",dpi=70)
    plt.close(fig)
# Example 7.1
I,M,D,A,P,S,V,O,H=.95,1,3.45,12.5,.54,.1,10,20,2.5
def lam(n,p=P): return D*(1-p)**n*A
def conf(n,m=M,p=P): l=lam(n,p); return sum(l**k/math.factorial(k) for k in range(m+1))*math.exp(-l)
def enc(n): return D*A*(1-(1-P)**n)
def passes(i,p,m=M):
    n=0
    while True:
        n+=1
        if not i>conf(n,m,p): return n
N=passes(I,P); Ns=np.arange(1,9)

# 1 Found vs remaining
fig,(ax,bx)=plt.subplots(1,2,figsize=(10.5,4.3),gridspec_kw={"width_ratios":[1.15,1]})
e=np.array([enc(n) for n in Ns]); l=np.array([lam(n) for n in Ns])
ax.bar(Ns,e,color=BLUE,alpha=.85,label="Found: E")
ax.bar(Ns,l,bottom=e,color=ORANGE,alpha=.9,label="Remaining: λ")
ax.axhline(D*A,color=INK,ls="--",lw=1); ax.text(.5,D*A+1.2,f"D × A = {D*A:.3f}",fontsize=9.5,ha="left")
ax.set_xticks(Ns); ax.set_xlabel("Passes N"); ax.set_ylabel("Mines"); ax.set_ylim(0,58); ax.set_xlim(.4,8.6)
ax.legend(frameon=False,loc="upper left",ncol=2,fontsize=9.5); ax.set_title("E + λ = D × A",loc="left",fontsize=12)
bx.semilogy(Ns,l,color=ORANGE,marker="o",lw=2.2)
bx.axhline(M,color=GREY,ls=":",lw=1.2); bx.text(8.3,M*1.18,f"M = {M}",ha="right",fontsize=9.5,color=GREY)
bx.plot(N,lam(N),"o",ms=12,mfc="none",mec=RED,mew=2)
bx.annotate(f"N = {N}: λ = {lam(N):.4f}",xy=(N,lam(N)),xytext=(1.3,.2),fontsize=10,color=RED,arrowprops=dict(arrowstyle="->",color=RED))
bx.text(3.9,4.5,f"Each pass leaves (1 − P) = {1-P:.2f}\nof the mines still in the area",fontsize=9.5)
bx.set_xticks(Ns); bx.set_xlabel("Passes N"); bx.set_ylabel("λ (log scale)"); bx.set_xlim(.6,8.4)
bx.set_title("λ = D × (1 − P)^N × A",loc="left",fontsize=12)
fig.suptitle("Found and Remaining Mines by Pass (Example 7.1)",x=.07,ha="left",fontweight="bold",fontsize=13)
fig.tight_layout(); save(fig,"found_vs_remaining")

# 2 Poisson distributions for N=5,6,7
fig,axs=plt.subplots(1,3,figsize=(10,3.9),sharey=True); ks=np.arange(0,5)
for ax,n in zip(axs,(5,6,7)):
    lv=lam(n); pm=[lv**k*math.exp(-lv)/math.factorial(k) for k in ks]
    ax.bar(ks,pm,color=[GREEN if k<=M else GREY for k in ks],alpha=.9)
    ok=conf(n)>=I
    ax.set_title(f"N = {n}:  λ = {lv:.3f}",loc="left",fontsize=11.5)
    ax.text(4.4,.93,f"C = {conf(n):.4f}",ha="right",fontsize=11,fontweight="bold",color=GREEN if ok else RED)
    ax.text(4.4,.84,"≥ 0.95  ✓" if ok else "< 0.95",ha="right",fontsize=10,color=GREEN if ok else RED)
    ax.set_xticks(ks); ax.set_xlabel("Mines remaining k"); ax.set_ylim(0,1)
axs[0].set_ylabel("Probability")
fig.suptitle("Confidence: sum of Poisson probabilities for k ≤ M (green), M = 1",x=.06,ha="left",fontweight="bold",fontsize=13)
fig.tight_layout(); save(fig,"poisson_confidence")

# 3 Confidence by pass for M = 0,1,2
fig,ax=plt.subplots(figsize=(8.5,4.4)); nn=np.arange(1,11)
for m,c in [(0,GREY),(1,BLUE),(2,GREEN)]:
    ax.plot(nn,[conf(n,m)*100 for n in nn],marker="o",ms=5,lw=2.2,color=c,label=f"M = {m}")
for lvl in (90,95,99): ax.axhline(lvl,color=INK,lw=.8,ls=":"); ax.text(10.15,lvl,f"{lvl}%",va="center",fontsize=9.5)
ax.plot(N,conf(N)*100,"o",ms=13,mfc="none",mec=ORANGE,mew=2.4)
ax.annotate(f"Example 7.1: stops at N = {N}\nC = {conf(N):.4f} ≥ 0.95",xy=(N,conf(N)*100),xytext=(7.7,48),fontsize=10,color=ORANGE,arrowprops=dict(arrowstyle="->",color=ORANGE))
ax.set_xticks(nn); ax.set_xlim(.6,10.8); ax.set_ylim(0,102); ax.set_xlabel("Passes N"); ax.set_ylabel("Confidence C (%)")
ax.legend(frameon=False,loc="center left",title="Max acceptable mines",fontsize=9.5,title_fontsize=9.5)
ax.set_title("Stopping Rule: add passes until C ≥ I",loc="left"); save(fig,"confidence_by_pass")

# 4 Time breakdown
fig,ax=plt.subplots(figsize=(8.5,4.4))
search=np.array([A*n/(V*S) for n in Ns]); disp=np.array([math.floor(enc(n)+.5)*H for n in Ns]); el=(search+disp)/O*24
ax.bar(Ns,search,color=BLUE,alpha=.85,label="Search: A × N ÷ (V × S)")
ax.bar(Ns,disp,bottom=search,color=ORANGE,alpha=.9,label="Disposal: E (rounded) × H")
ax.plot(Ns,el,color=INK,marker="D",ms=5,lw=1.6,label=f"T: elapsed hours at {O} h/day")
ax.annotate(f"N = {N}: {search[N-1]:.1f} + {disp[N-1]:.1f} = {search[N-1]+disp[N-1]:.1f} operating h\nT = {el[N-1]:.0f} elapsed h ({el[N-1]/24:.2f} days)",
            xy=(N,el[N-1]),xytext=(4.3,300),fontsize=9.5,arrowprops=dict(arrowstyle="->",color=INK))
ax.set_xticks(Ns); ax.set_xlabel("Passes N"); ax.set_ylabel("Hours"); ax.set_xlim(.4,8.6); ax.set_ylim(0,330)
ax.legend(frameon=False,loc="upper left",fontsize=9.5)
ax.set_title("Mission Time: search plus disposal, scaled to elapsed time",loc="left"); save(fig,"time_breakdown")

# 5 Planning sensitivity: passes vs P
fig,ax=plt.subplots(figsize=(8.5,4.4)); ps=np.round(np.arange(.40,.901,.01),2)
for lvl,c in [(.90,GREEN),(.95,BLUE),(.99,ORANGE)]:
    ax.step(ps*100,[passes(lvl,p) for p in ps],where="mid",lw=2.2,color=c,label=f"I = {lvl:.2f}")
ax.plot(P*100,N,"o",ms=11,mfc="none",mec=RED,mew=2.2); ax.annotate(f"Example 7.1\nP = {P:.2f}, N = {N}",xy=(P*100,N),xytext=(60,11),fontsize=10,color=RED,arrowprops=dict(arrowstyle="->",color=RED))
ax.set_xlabel("Detection probability per pass P (%)"); ax.set_ylabel("Passes required N"); ax.set_xlim(40,90)
ax.set_yticks(range(0,15,2)); ax.legend(frameon=False,loc="upper right",fontsize=9.5,title="Intended confidence",title_fontsize=9.5)
ax.set_title(f"Planning Sensitivity: passes required (D = {D}, A = {A}, M = {M})",loc="left"); save(fig,"passes_vs_detection")
print("N",N,"search",search[N-1],"disp",disp[N-1],"T",el[N-1])
