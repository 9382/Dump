return(function(a)local b,c,d,e=string.sub,string.byte,string.rep,string.char;local f,g=math.floor,math.log;local h,i,j,k,l,m,n,o,p=type,pairs,select,unpack,getfenv,error,tonumber,tostring,assert;local q,r,s=true,false,nil;local t;local u;local function v(w)local x={}x.P=w;x.L={}function x:GL(y)local z=x.L[y]if z then return z end;if x.P then local A=x.P:GL(y)if A then return A end end;return s end;function x:SL(y,B)local C=x:GL(y)if not C then m("Bad SL "..o(y))end;C[16]=B end;function x:ML(y,B)local z={}z.S=x;z[0]=y;z[16]=B;x.L[y]=z;return z end;return x end;local D=__ENV or l()local E={}local function F(G,...)local H=E[G]or{1,1}local I={...}local J=H[1]for K=J,H[2]do G[K]=s end;for K=1,j("#",...)do G[J]=I[K]J=J+1 end;E[G]={H[1]+1,J}end;u=function(L,x,M)local N=L[7]if N==2 then if M then return L,q else local O=x:GL(L[0])if not O then if L[17]then m("Expected '"..o(L[0]).."' was missing")end else return O[16]end;return D[L[0]]end elseif N==8 then return n(L[16][29])elseif N==9 then return L[16][29]elseif N==11 then return L[16]elseif N==10 then return s elseif N==15 then local P=u(L[8],x)local Q=u(L[9],x)local R=L[12]if R==1 then return P+Q elseif R==2 then return P-Q elseif R==3 then return P%Q elseif R==4 then return P/Q elseif R==5 then return P*Q elseif R==6 then return P^Q elseif R==7 then return P..Q elseif R==8 then return P==Q elseif R==9 then return P<Q elseif R==10 then return P<=Q elseif R==11 then return P~=Q elseif R==12 then return P>Q elseif R==13 then return P>=Q elseif R==14 then return P and Q elseif R==15 then return P or Q end elseif N==14 then local Q=u(L[9],x)local R=L[12]if R==1 then return-Q elseif R==2 then return not Q elseif R==3 then return#Q end elseif N==12 then return k(x:GL("...")[16])elseif N==5 or N==7 or N==6 then local S={}for T,U in i(L[3])do if N==6 then S={U[29]}else F(S,u(U,x))end end;return u(L[5],x)(k(S))elseif N==4 then if M then return L,q else return u(L[5],x)[u(L[2],x)]end elseif N==3 then if M then return L,q else if L[6]==r then return u(L[5],x)[L[4][29]]elseif L[6]==q then local V=u(L[5],x)local W=V[L[4][29]]if h(W)=="function"then return function(...)return W(V,...)end else return W end end end elseif N==1 then return function(...)local X=v(x)local Y={...}for K=1,#L[3]do local U=L[3][K]if U then X:ML(U[0],Y[K])end end;if L[14]then local Z={}for K=#L[3]+1,#Y do Z[#Z+1]=Y[K]end;X:ML("...",Z)end;local _=t(L[1],X)if not _ then return elseif _.T==1 then return k(_.D)else local a0=_.T==2 and"break"or"continue"m("Illegal attempt to "..a0 .." the current scope")end end elseif N==13 then local W={}for T,a1 in i(L[13])do if a1[27]==0 then W[u(a1[28],x)]=u(a1[16],x)elseif a1[27]==1 then W[a1[28]]=u(a1[16],x)end end;for T,a1 in i(L[13])do if a1[27]==2 then F(W,u(a1[16],x))end end;return W end end;local a2=function(a0)local N=a0[7]if N==12 then local W={}for K=1,#a0[9]do F(W,u(a0[9][K],a0.S))end;for K=1,#a0[8]do local P,a3=u(a0[8][K],a0.S,q)local Q=W[K]if a3 then if P[7]==2 then if P[17]then a0.S:SL(P[0],Q)else D[P[0]]=Q end elseif P[7]==3 then local V=u(P[5],a0.S)V[P[4][29]]=Q else local V=u(P[5],a0.S)V[u(P[2],a0.S)]=Q end end end elseif N==13 then u(a0[21],a0.S)elseif N==8 then local W={}for K=1,#a0[15]do F(W,u(a0[15][K],a0.S))end;for K=1,#a0[18]do local C=a0[18][K]a0.S:ML(C[0],W[K])end elseif N==2 then for T,a4 in i(a0[11])do if not a4[10]or u(a4[10],a0.S)then return t(a4[1],v(a0.S))end end elseif N==3 then while u(a0[10],a0.S)do local _=t(a0[1],v(a0.S))if _ then if _.T==2 then return elseif _.T==1 then return _ end end end elseif N==4 then return t(a0[1],v(a0.S))elseif N==9 then local a5={}for T,U in i(a0[3])do F(a5,u(U,a0.S))end;return a5 elseif N==10 then return q elseif N==11 then return r elseif N==7 then repeat local _=t(a0[1],v(a0.S))if _ then if _.T==2 then return elseif _.T==1 then return _ end end until u(a0[10],a0.S)elseif N==1 then local y=a0[0]if y[7]==3 then if y[6]==r then local V=u(y[5],a0.S)local a6=u(a0,a0.S)V[y[4][29]]=a6 elseif y[6]==q then for K=#a0[3],1,-1 do a0[3][K+1]=a0[3][K]end;a0[3][1]={[0]="self",[17]=q}local V=u(y[5],a0.S)local a6=u(a0,a0.S,q)V[y[4][29]]=a6 end else local a6=u(a0,a0.S)if a0[22]then a0.S:ML(y[0],a6)else D[y[0]]=a6 end end elseif N==6 then local a7,a8,a9;local aa=a0[19]if not aa[2]then a7,a8,a9=u(aa[1],a0.S)else a7=u(aa[1],a0.S)a8=u(aa[2],a0.S)if aa[3]then a9=u(aa[3],a0.S)end end;while q do local X=v(a0.S)local S={a7(a8,a9)}a9=S[1]if a9==s then break end;for K=1,#S do X:ML(a0[20][K][0],S[K])end;local _=t(a0[1],X)if _ then if _.T==2 then return elseif _.T==1 then return _ end end end elseif N==5 then local ab=n(u(a0[23],a0.S))local ac=n(u(a0[24],a0.S))local ad=a0[25]and n(u(a0[25],a0.S))or 1;while ad>0 and ab<=ac or ad<=0 and ab>=ac do local X=v(a0.S)X:ML(a0[26][0],ab)local _=t(a0[1],X)if _ then if _.T==2 then return elseif _.T==1 then return _ end end;ab=ab+ad end end end;t=function(ae,x)for T,af in i(ae[1])do af.S=x;local W=a2(af)if h(W)=="table"then if not W.P then return{P=q,T=1,D=W}else return W end elseif h(W)=="boolean"then return{P=q,T=W==q and 2 or 3}end end end;return function()a=(function(ag)local function ah(ai,aj,ak)return d(ak,aj-#ai)..ai end;local function al(am)return n(am,2)end;local function an(aj,ao)p(f(aj)==aj)if aj==0 then return ah("0",ao or 1,"0")end;local ap=f(g(aj,2))local aq=""while ap>=0 do if aj>=2^ap then aj=aj-2^ap;aq=aq.."1"else aq=aq.."0"end;ap=ap-1 end;return ah(aq,ao or 1,"0")end;local function ar(as)local ap=0;local at=0;for au=1,#as do local av=b(as,au,au)if av=="1"then at=at+2^ap end;ap=ap-1 end;return at end;local aw=ag;local ax=""local function ay(az)for K=1,f((az-#ax-1)/6)+1 do ax=ax..b(an(c(aw,1,1),8),3,-1)aw=b(aw,2,-1)end end;local function aA(az)ay(az)local aB=b(ax,1,az)ax=b(ax,az+1)return aB end;local function aC(az)return al(aA(az))end;local function aD()return e(aC(8))end;local function aE()local aF,aG,aH=aC(1),aC(11),aA(52)aF,aG=aF==0 and 1 or-1,2^(aG-1023)return aF*aG*ar("1"..aH)end;local aI=0;local aJ=1;local aK=2;local aL=3;local aM=4;local aN=5;local aO=6;local aP=7;local aQ=3;local function aR(aS)if not aS then p(aC(aQ)==aI,"Invalid SD")end;local aT={}local aU=s;local function aV(aW)if aU then aT[aU]=aW;aU=s else aU=aW end end;while q do local aX=aC(aQ)if aX==aJ then return aT elseif aX==aI then aV(aR(q))elseif aX==aK then local aY=""while q do local aZ=aD()if aZ=="\0"then aV(aY)break elseif aZ=="\\"then aY=aY..aD()else aY=aY..aZ end end elseif aX==aL then aV(aE())elseif aX==aM then aV(aC(1)==1)elseif aX==aN then aV(aC(4))elseif aX==aO then aV(aC(3))elseif aX==aP then aV(aC(5))end end end;return aR()end)(a)local _=t(a,v())if not _ then return elseif _.T==1 then return k(_.D)else local a0=_.T==2 and"break"or"continue"m("Illegal attempt to "..a0 .." the current scope")end end end)([=[]=])()