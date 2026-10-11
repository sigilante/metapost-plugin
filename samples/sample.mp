% MetaPost highlighting sample
prologues := 3;
outputformat := "svg";
outputtemplate := "%j-%c.svg";

input boxes;

vardef midpoint(expr a, b) = .5[a, b] enddef;
def stroke_it(expr p) text t = draw p t; enddef;
primarydef w dotprod z = (xpart w * xpart z + ypart w * ypart z) enddef;

beginfig(1);
  numeric u; u := 1cm;
  pair A, B;
  path p;
  z1 = (0, 0); z2 = (3u, 2u);
  p := z1{dir 30} .. z2 -- cycle;
  for i = 1 upto 3:
    draw p scaled (i * .5) withcolor (i/3) * red withpen pencircle scaled 0.4pt;
  endfor
  if known A: label.top(btex $\alpha^2$ etex, A); else: dotlabel.lft("B", z2); fi
  fill fullcircle scaled 2mm shifted z1 withcolor .8white;
endfig;
end
