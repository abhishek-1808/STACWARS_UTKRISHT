import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.family":"serif","font.serif":["Liberation Serif"],"font.size":8})
d1=list(range(21)); f1=[1]*21
for t in (3,8,12,16,20): f1[t]=0.9970
t2=[0,20,40,60,80,100,120,140,160,180,200]; f2=[1]*11
for t in (20,100,180): f2[t//20]=0.9990
t3=list(range(0,201,10)); f3=[1.0]*21
for t,v in {20:.9990,60:.9992,100:.9991,140:.9993,170:.9990}.items(): f3[t//10]=v
fig,ax=plt.subplots(3,1,figsize=(3.45,4.6))
for a,(t,f,n,pt) in zip(ax,[(d1,f1,"STAC-1",[3,8,12,16,20]),(t2,f2,"STAC-2",[20,100,180]),(t3,f3,"STAC-3",[20,60,100,140,170])]):
    a.plot(t,f,"-",color="0.7",lw=.6)
    a.plot(t,f,"o",ms=3,color="k")
    a.plot(pt,[f[t.index(p)] for p in pt],"o",ms=4.5,mfc="none",mec="crimson",mew=1)
    a.axhline(1,color="0.5",ls="--",lw=.5)
    a.set_ylabel("Rel. brightness"); a.text(.02,.12,n,transform=a.transAxes,fontweight="bold")
    a.set_ylim(min(f)-.0012,1.0008); a.ticklabel_format(axis="y",useOffset=False)
ax[2].set_xlabel("Time (days)")
for a in ax: a.tick_params(labelsize=7)
plt.tight_layout(); plt.savefig("../figures/lc.pdf")
