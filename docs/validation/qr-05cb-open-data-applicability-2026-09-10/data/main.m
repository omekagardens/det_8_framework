%% Read File
clear;
filename='VBI_Coincidence_20230707.dat';
RawData=textread(filename);
beta_step=32;  % steps of beta
alpha_step=length(RawData(:,9))/beta_step; % steps of alpha
CC4=reshape(RawData(:,9),beta_step,alpha_step)';
Alice=reshape(RawData(:,10),beta_step,alpha_step)';
Bob=reshape(RawData(:,11),beta_step,alpha_step)';

%% All data analyze
figure(4)
set (gcf,'Position',[50,50,1000,350], 'color','w')
lw=1;
ms=7;
fs=15;
c=0;
fst = 18;
maxCC=max(CC4');
minCC=min(CC4');
vis=(maxCC-minCC)./(maxCC+minCC);
det=(sqrt(maxCC).*minCC+sqrt(minCC).*maxCC)./(maxCC+minCC).^2;
subplot(1,2,1)
f1=errorbar(1:1:37,vis,det,'o','LineWidth',lw,...
    'MarkerEdgeColor','black',...
    'MarkerFaceColor',[0.8 0.8 0.8],...
    'MarkerSize',ms,...
    'CapSize',c,...
    'color',[0, 0, 0]/255);
hold
f1=errorbar(1:1:37,vis,det,'o','MarkerSize',ms,'color',[0, 0, 0]/255,'CapSize',c,'LineWidth',lw);
axis([0,37,0,1])
set(gca,'XTick',[0,8,16,24,32],'XTickLabel',{'0','4\pi','8\pi','12\pi','16\pi'},'FontSize',fs);
xlabel('\alpha','FontSize',fs);
ylabel('Visibility','FontSize',fs);
plot([0,37],[1/sqrt(2),1/sqrt(2)],'--','LineWidth',lw,'color',[255,99,71]/255);
title('A','position',[-6,0.95],'FontSize',fst)

subplot(1,2,2)
% cycles=reshape(CC4',8,32*37/8);
% maxCC=max(CC4');
% minCC=min(CC4');
% vis=(maxCC-minCC)./(maxCC+minCC);
step=0.0181;
start=0.72;
distribution=start:step:(start+step*15);
A=zeros(1,length(distribution));
for j=1:1:length(distribution)
    for i=1:1:length(vis)
        if abs(vis(i)-distribution(j))<step/2
            A(j)=A(j)+1;
        end
    end
end
bar(distribution,A,'FaceColor',[255,99,71]/255,'EdgeColor',[0,0,0]/255,'LineWidth',1)
axis([0.69,0.93,0,12]);
set(gca,'XTick',[0.7,0.75,0.8,0.85,0.9],'XTickLabel',{'0.7','0.75','0.8','0.85','0.9'},'FontSize',fs);
xlabel('Visibility','FontSize',fs);
ylabel('Occurence','FontSize',fs);
hold;
plot([1/sqrt(2),1/sqrt(2)],[0,15],'--','LineWidth',lw,'color',[255,99,71]/255);
title('B','position',[0.652,11.4],'FontSize',fst)

%% Valid data
%%%%%%%%%%% valid data %%%%%%%%%%%%%%%%
sub_CC4=CC4(5:8,:);
sub_CC4=flip(sub_CC4,1);

%% Submatrix Plot
figure(1)
set (gcf,'Position',[50,50,1000,250], 'color','w')
h=bar3(sub_CC4);
for i=1:numel(h)
    zdata=h(i).ZData;
    h(i).CData=zdata;
    h(i).FaceColor='interp';
end
zlim([0,420]);
set(gca,'XTick',[2,10,18,26],'XTickLabel',{'0','2\pi','4\pi','6\pi'},'FontSize',16);
xlabel('\beta','FontSize',16);
set(gca,'YTick',[1,2,3,4],'YTickLabel',{'3\pi/2','\pi','\pi/2','0'},'FontSize',16);
ylabel('\alpha','FontSize',16);
set(gca,'ZTick',[0,209,418],'ZTickLabel',{'0','209','418'},'FontSize',16);
zlabel('Four-photon Coincidence','FontSize',16);
axis([0.5,32.5,0,4.5])
colorbar;

clear color_map
color_map=importdata('colormap.txt');
% 此处只取前列即可。
YlGn=color_map(:,1:3);
colormap(YlGn);shading interp;

caxis([0,max(max(sub_CC4))]);
colorbar('Ticks',[0,200,max(max(sub_CC4))]);



%%  Counts Line
sub_CC4=CC4(5:8,:);
%sub_CC4=flip(sub_CC4,1);

figure(2)
x=0.15*pi:77/300*pi:4*pi;
fs=15;
fs2=15;
w=1;
m=7;
c=0;
set (gcf,'Position',[50,50,1200,280], 'color','w')

subplot(1,2,1)

Counts1=sub_CC4(1,1:16);
F1=fit(x',Counts1','a*sin(b*x+c)+d','startpoint',[100,1,pi,200]);
f1=errorbar(x,Counts1,sqrt(Counts1),'o','MarkerSize',m,...
    'MarkerEdgeColor','black',...
    'MarkerFaceColor',[0.8 0.8 0.8],...
    'CapSize',c,...
    'LineWidth',w,...
    'color',[0, 0, 0]/255);
hold;
p1=plot(F1);
set(p1,'color',[0, 0, 0]/255);
p1.LineWidth=w;
p1=plot(x,Counts1,'o','color',[0, 0, 0]/255,'LineWidth',w,'MarkerSize',m,'MarkerFaceColor',[0.8 0.8 0.8]);

f1=errorbar(x,Counts1,sqrt(Counts1),'o','MarkerSize',m,'color',[0, 0, 0]/255,'CapSize',c','LineWidth',w);

ma1=max(Counts1);
mi1=min(Counts1);
vis1=(ma1-mi1)/(ma1+mi1);
vis1_det=(ma1*sqrt(mi1)+mi1*sqrt(ma1))/(ma1+mi1)^2;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Counts3=sub_CC4(3,1:16);
F3=fit(x',Counts3','a*sin(b*x+c)+d','startpoint',[-100,1,pi,200]);
p3=plot(F3,'--');
set(p3,'color',[255,99,71]/255);
p3.LineWidth=w;
p3=plot(x,Counts3,'^','color',[255,99,71]/255,'LineWidth',w,'MarkerSize',m,'MarkerFaceColor',[255,200,200]/255);

f3=errorbar(x,Counts3,sqrt(Counts3),'^','MarkerSize',m,...
    'MarkerEdgeColor',[255,99,71]/255,...
    'MarkerFaceColor',[255,200,200]/255,...
    'CapSize',c,...
    'LineWidth',w,...
    'color',[255,99,71]/255);
f3=errorbar(x,Counts3,sqrt(Counts3),'^','MarkerSize',m,'color',[255, 99, 71]/255,'CapSize',c','LineWidth',w);

ma3=max(Counts3);
mi3=min(Counts3);
vis3=(ma3-mi3)/(ma3+mi3);
vis3_det=(ma3*sqrt(mi3)+mi3*sqrt(ma3))/(ma3+mi3)^2;

set(gca,'XTick',[0,2*pi,4*pi,6*pi,8*pi],'XTickLabel',{'0','2\pi','4\pi','6\pi','8\pi'},'FontSize',fs);
xlabel('\beta','FontSize',fs);
ylabel('4-photon C. C.','FontSize',fs);
axis([0,4*pi,0,500])
le1=legend([p1,p3],{'\alpha=0','\alpha=\pi'},'FontSize',fs);
legend boxoff
set(le1,'unit','centimeters','position',[13,5.9,0.4,0.7]);
title('A','position',[-2,450],'FontSize',fst)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
subplot(1,2,2);
x=pi/4:pi/4:4*pi;

Counts2=sub_CC4(2,1:16);
F2=fit(x',Counts2','a*sin(b*x+c)+d','startpoint',[100,1,pi,200]);
f2=errorbar(x,Counts2,sqrt(Counts2),'o','MarkerSize',m,...
    'MarkerEdgeColor','black',...
    'MarkerFaceColor',[0.8 0.8 0.8],...
    'CapSize',c,...
    'LineWidth',w,...
    'color',[0, 0, 0]/255);
hold;
p2=plot(F2);
set(p2,'color',[0, 0, 0]/255);
p2.LineWidth=w;
p2=plot(x,Counts2,'o','color',[0, 0, 0]/255,'LineWidth',w,'MarkerSize',m,'MarkerFaceColor',[0.8 0.8 0.8]);

f2=errorbar(x,Counts2,sqrt(Counts2),'o','MarkerSize',m,'color',[0, 0, 0]/255,'CapSize',c','LineWidth',w);

ma2=max(Counts2);
mi2=min(Counts2);
vis2=(ma2-mi2)/(ma2+mi2);
vis2_det=(ma2*sqrt(mi2)+mi2*sqrt(ma2))/(ma2+mi2)^2;

%%%%%%%%%%%%%%%
Counts4=sub_CC4(4,1:16);
F4=fit(x',Counts4','a*sin(b*x+c)+d','startpoint',[100,1,pi,200]);
p4=plot(F4,'--');
set(p4,'color',[255,99,71]/255);
p4.LineWidth=w;
p4=plot(x,Counts4,'^','color',[255,99,71]/255,'LineWidth',w,'MarkerSize',m,'MarkerFaceColor',[255,200,200]/255);

f4=errorbar(x,Counts4,sqrt(Counts4),'^','MarkerSize',m,...
    'MarkerEdgeColor',[255,99,71]/255,...
    'MarkerFaceColor',[255,200,200]/255,...
    'CapSize',c,...
    'LineWidth',w,...
    'color',[255,99,71]/255);
f4=errorbar(x,Counts4,sqrt(Counts4),'^','MarkerSize',m,'color',[255,99,71]/255,'CapSize',c','LineWidth',w);

ma4=max(Counts4);
mi4=min(Counts4);
vis4=(ma4-mi4)/(ma4+mi4);
vis4_det=(ma4*sqrt(mi4)+mi4*sqrt(ma4))/(ma4+mi4)^2;

set(gca,'XTick',[0,2*pi,4*pi,6*pi,8*pi],'XTickLabel',{'0','2\pi','4\pi','6\pi','8\pi'},'FontSize',fs);
xlabel('\beta','FontSize',fs);
ylabel('4-photon C. C.','FontSize',fs);
axis([0,4*pi,0,500])
le=legend([p2,p4],{'\alpha=\pi/2','\alpha=3\pi/2'},'FontSize',fs);
legend boxoff
set(le,'unit','centimeter','position',[27,5.9,0.4,0.7]);
title('B','position',[-2,450],'FontSize',fst)
 %% Correlation Function Line1
msize=7;
ll=1;

figure(3)
set (gcf,'Position',[50,50,1200,400], 'color','w')
subplot(1,2,1)
Counts=CC4(5:8,:);
Curve1=[];
Curve2=[];
detCurve1=[];
detCurve2=[];
for i=1:1:beta_step-4
    Curve1(i)=(Counts(1,i)+Counts(3,i+4)-Counts(1,i+4)-Counts(3,i))/(Counts(1,i)+Counts(3,i+4)+Counts(1,i+4)+Counts(3,i));
    detCurve1(i)=2*((Counts(1,i)+Counts(3,i+4))*sqrt(Counts(1,i+4)+Counts(3,i))+(Counts(1,i+4)+Counts(3,i))*sqrt(Counts(1,i)+Counts(3,i+4)))/(Counts(1,i)+Counts(3,i+4)+Counts(1,i+4)+Counts(3,i))^2;
    Curve2(i)=(Counts(2,i)+Counts(4,i+4)-Counts(2,i+4)-Counts(4,i))/(Counts(2,i)+Counts(4,i+4)+Counts(2,i+4)+Counts(4,i));
    detCurve2(i)=2*((Counts(2,i)+Counts(4,i+4))*sqrt(Counts(2,i+4)+Counts(4,i))+(Counts(2,i+4)+Counts(4,i))*sqrt(Counts(2,i)+Counts(4,i+4)))/(Counts(2,i)+Counts(4,i+4)+Counts(2,i+4)+Counts(4,i))^2;
end
% fit of exp data
x=pi/4:pi/4:7*pi;
F1=fit(x',Curve1','a*sin(b*x+c)+d','startpoint',[0.8,1,pi,0]);
F2=fit(x',Curve2','a*sin(b*x+c)+d','startpoint',[0.8,1,pi,0]);

% plot all the curves
f1=errorbar(x,Curve1,detCurve1,'o','MarkerSize',msize,...
    'MarkerEdgeColor','black',...
    'MarkerFaceColor',[0.8 0.8 0.8],...
    'CapSize',c,...
    'LineWidth',w,...
    'color',[0, 0, 0]/255);
hold;
p1=plot(F1);
set(p1,'color',[0,0,0]/255);
p1.LineWidth=ll;
p1=plot(x,Curve1,'o','color',[0,0,0]/255,'LineWidth',ll,'MarkerSize',msize,'MarkerFaceColor',[0.8 0.8 0.8]);

f1=errorbar(x,Curve1,detCurve1,'o','MarkerSize',msize,'color',[0, 0, 0]/255,'CapSize',c','LineWidth',w);



%% Correlation Function Line2
p2=plot(F2,'--');
set(p2,'color',[255,99,71]/255);
p2.LineWidth=ll;
p2=plot(x,Curve2,'^','color',[255,99,71]/255,'LineWidth',ll,'MarkerSize',msize, 'MarkerFaceColor',[255,200,200]/255);

f2=errorbar(x,Curve2,detCurve2,'^','MarkerSize',msize,...
    'MarkerEdgeColor',[255,99,71]/255,...
    'MarkerFaceColor',[255,200,200]/255,...
    'CapSize',c,...
    'LineWidth',w,...
    'color',[255,99,71]/255);
f2=errorbar(x,Curve2,detCurve2,'^','MarkerSize',msize,'color',[255,99,71]/255,'CapSize',c','LineWidth',w);



long_y=1/sqrt(2);
p3=plot([0,7*pi],[long_y,long_y],':','color','k');
p4=plot([0,7*pi],[-long_y,-long_y],':','color','k');
p3.LineWidth=0.5;
p4.LineWidth=0.5;

legend([p1,p2],{'\alpha=0','\alpha=\pi/2'},'FontSize',fs2);
legend boxoff;

axis([0,4*pi,-1,1.2])
set(gca,'xtick',[0 2*pi 4*pi 6*pi])
set(gca,'XTickLabel',{'0','2\pi','4\pi','6\pi'},'FontSize', fs2,'Fontname','Helvetica')
xlabel('\beta');
ylabel('Correlation Function');
title('A','position',[-2,1],'FontSize',fst)
%% Single Counts
subplot(1,2,2)
beta=pi/4:pi/4:8*pi;
sub_Alice=Alice(5:8,:);
pa=plot(beta,Alice(1,:),'s','color',[0,0,0],'MarkerSize',msize,...
    'MarkerEdgeColor','black',...
    'MarkerFaceColor',[0.8 0.8 0.8]);
hold;
pb=plot(beta,Bob(1,:),'diamond','color',[255,99,71]/255,'MarkerSize',msize,...
    'MarkerEdgeColor',[255,99,71]/255,...
    'MarkerFaceColor',[255,200,200]/255);

axis([0,7*pi,0.5*10^6,2*10^6]);

set(gca,'xtick',[0 2*pi 4*pi 6*pi]);
set(gca,'XTickLabel',{'0','2\pi','4\pi','6\pi'},'FontSize', fs2,'Fontname','Helvetica');
xlabel('\beta');
ylabel('Local Two-Fold C. C.');

aveAlice=mean(Alice(1,:));
aveBob=mean(Bob(1,:));
pal=plot([0,7*pi],[aveAlice,aveAlice],'-','color',[0,0,0]);
pbl=plot([0,7*pi],[aveBob,aveBob],'-','color',[255,99,71]/255);
pa.LineWidth=ll;
pb.LineWidth=ll;
pal.LineWidth=ll;
pbl.LineWidth=ll;

legend([pa,pb],{'Alice','Bob'},'FontSize',fs2);
legend boxoff;
title('B','position',[-3.5,1.85*10^6],'FontSize',fst)
[m1,i1]=max(Curve1)
d1=detCurve1(i1)
[m2,i2]=max(Curve2)
d2=detCurve2(i2)

%% Other parameter S
S2=-Curve1(11)+Curve1(13)+Curve2(11)+Curve2(13);
detS2=-detCurve1(11)+detCurve1(13)+detCurve2(11)+detCurve2(13);

S3=-Curve1(19)+Curve1(21)+Curve2(19)+Curve2(21);
detS3=-detCurve1(19)+detCurve1(21)+detCurve2(19)+detCurve2(21);
%% All parameter S
Total=flip(sub_CC4(:,2:9)+sub_CC4(:,10:17)+sub_CC4(:,18:25),1);
E1=(Total(1,2)+Total(3,6)-Total(1,6)-Total(3,2))/(Total(1,2)+Total(3,6)+Total(1,6)+Total(3,2));
E2=(Total(1,4)+Total(3,8)-Total(1,8)-Total(3,4))/(Total(1,4)+Total(3,8)+Total(1,8)+Total(3,4));
E3=(Total(2,2)+Total(4,6)-Total(2,6)-Total(4,2))/(Total(2,2)+Total(4,6)+Total(2,6)+Total(4,2));
E4=(Total(2,4)+Total(4,8)-Total(2,8)-Total(4,4))/(Total(2,4)+Total(4,8)+Total(2,8)+Total(4,4));

a=Total(1,2);
b=Total(3,6);
c=Total(1,6);
d=Total(3,2);
detE1=2/(a+b+c+d)^2*((c+d)*(sqrt(a+b))+(a+b)*(sqrt(c+d)));


a=Total(1,4);
b=Total(3,8);
c=Total(1,8);
d=Total(3,4);
detE2=2/(a+b+c+d)^2*((c+d)*(sqrt(a+b))+(a+b)*(sqrt(c+d)));

a=Total(2,2);
b=Total(4,6);
c=Total(2,6);
d=Total(4,2);
detE3=2/(a+b+c+d)^2*((c+d)*(sqrt(a+b))+(a+b)*(sqrt(c+d)));

a=Total(2,4);
b=Total(4,8);
c=Total(2,8);
d=Total(4,4);
detE4=2/(a+b+c+d)^2*((c+d)*(sqrt(a+b))+(a+b)*(sqrt(c+d)));

-detE1+detE2+detE3+detE4
-E1+E2+E3+E4

%% visibilities
mean(vis)
mean(det)