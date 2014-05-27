# Create Job CD decomposition from Census BDS data

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from __future__ import division
import brewer2mpl

# Get "Set2" colors from ColorBrewer (all colorbrewer scales: http://bl.ocks.org/mbostock/5577023)
Colors = brewer2mpl.get_map('RdPu', 'sequential', 9).mpl_colors

def AddAggregateData(LeftData):
	LeftData = LeftData.merge(AllData[['year2','JC','JD']].rename(columns={'JC':'JC_All','JD':'JD_All'}),on='year2')
	return LeftData
def AddSICData(LeftData):
	LeftData = LeftData.merge(SICData[['year2','sic1','JC','JD']].rename(columns={'JC':'JC_All','JD':'JD_All'}),on=['year2','sic1'],how='left')
	return LeftData
def FixSizeStrings(size_str):
	fix_str = '20'
	if size_str == 'a) 1 to 4':
		fix_str = '1-4'
	elif size_str == 'b) 5 to 9':
		fix_str = '5-9'
	elif size_str == 'c) 10 to 19':
		fix_str = '10-19'
	elif size_str == 'd) 20 to 49':
		fix_str = '20-49'
	elif size_str == 'e) 50 to 99':
		fix_str = '50-99'
	elif size_str == 'f) 100 to 249':
		fix_str = '100-249'
	elif size_str == 'g) 250 to 499':
		fix_str = '250-499'
	elif size_str == 'h) 500 to 999':
		fix_str = '500-999'
	elif size_str == 'i) 1000 to 2499':
		fix_str = '1000-2499'
	elif size_str == 'k) 2500 to 9999':
		fix_str = '2500-9999'
	elif size_str == 'l) 10000+':
		fix_str = 'l) 10000+'
	return fix_str
# Aggregate data

AgeData = pd.read_csv('/Users/allentran/Dropbox/Research/Retail/Data/bds_f_age_release.csv')
AgeData = AgeData[['year2','fage4','Emp','d_flag']]
I = ~np.isnan(AgeData.Emp)
AgeData = AgeData.loc[I,:]

Data = pd.read_csv('/Users/allentran/Dropbox/Research/Retail/Data/bds_f_all_release.csv')
Data = Data[['year2','emp','job_creation','job_creation_births',
'job_creation_continuers','job_destruction','job_destruction_deaths','job_destruction_continuers','firmdeath_emp','net_job_creation']]
Data = Data.fillna(value=0)

JC_firmbirths = AgeData[AgeData.fage4 == 'a) 0'][['year2','Emp']]
JC_firmbirths = JC_firmbirths.rename(columns={'Emp':'JC_firmbirths'})

AllData = JC_firmbirths.merge(Data,on=['year2'])

AllData['JC_EstabBirth'] = AllData['job_creation_births'] - AllData['JC_firmbirths']
AllData['JD_EstabDeath'] = AllData['job_destruction_deaths'] - AllData['firmdeath_emp']
AllData['JC'] = AllData['JC_firmbirths'] + AllData['JC_EstabBirth'] + AllData['job_creation_continuers']
AllData['JD'] = AllData['firmdeath_emp'] + AllData['JD_EstabDeath'] + AllData['job_destruction_continuers']

# Details on SIC

AgeData = pd.read_csv('/Users/allentran/Dropbox/Research/Retail/Data/bds_f_agesic_release.csv')
AgeData = AgeData[['year2','sic1','fage4','Emp','d_flag']]
I = ~np.isnan(AgeData.Emp)
AgeData = AgeData.loc[I,:]

Data = pd.read_csv('/Users/allentran/Dropbox/Research/Retail/Data/bds_f_sic_release.csv')
Data = Data[['year2','emp','sic1','net_job_creation','job_creation','job_creation_births',
'job_creation_continuers','job_destruction','job_destruction_deaths','job_destruction_continuers','firmdeath_emp','d_flag']]
I = Data.d_flag == 0
Data = Data.loc[I,:]
Data = Data.fillna(value=0)

JC_firmbirths = AgeData[AgeData.fage4 == 'a) 0'][['year2','sic1','Emp']]
JC_firmbirths = JC_firmbirths.rename(columns={'Emp':'JC_firmbirths'})

SICData = JC_firmbirths.merge(Data,on=['sic1','year2'])

SICData['JC_EstabBirth'] = SICData['job_creation_births'] - SICData['JC_firmbirths']
SICData['JD_EstabDeath'] = SICData['job_destruction_deaths'] - SICData['firmdeath_emp']
SICData['JC'] = SICData['JC_firmbirths'] + SICData['JC_EstabBirth'] + SICData['job_creation_continuers']
SICData['JD'] = SICData['firmdeath_emp'] + SICData['JD_EstabDeath'] + SICData['job_destruction_continuers']

R = SICData['sic1'] == 52
M = SICData['sic1'] == 20
RetailData = SICData.loc[R,:]
ManData = SICData.loc[M,:]

# Firm size

AgeData = pd.read_csv('/Users/allentran/Dropbox/Research/Retail/Data/bds_f_agesz_release.csv')
AgeData = AgeData[['year2','fsize','fage4','emp','d_flag']]
I = ~np.isnan(AgeData.emp)
AgeData = AgeData.loc[I,:]

Data = pd.read_csv('/Users/allentran/Dropbox/Research/Retail/Data/bds_f_sz_release.csv')
Data = Data[['year2','Emp','fsize','Net_Job_Creation','Job_Creation','Job_Creation_Births',
'Job_Creation_Continuers','Job_Destruction','Job_Destruction_Deaths','Job_Destruction_Continuers','firmdeath_emp','d_flag']]
I = Data.d_flag == 0
Data = Data.loc[I,:]
Data = Data.fillna(value=0)

JC_firmbirths = AgeData[AgeData.fage4 == 'a) 0'][['year2','fsize','emp']]
JC_firmbirths = JC_firmbirths.rename(columns={'emp':'JC_firmbirths'})

SZData = JC_firmbirths.merge(Data,on=['fsize','year2'])

SZData['JC_EstabBirth'] = SZData['Job_Creation_Births'] - SZData['JC_firmbirths']
SZData['JD_EstabDeath'] = SZData['Job_Destruction_Deaths'] - SZData['firmdeath_emp']
SZData['JC'] = SZData['JC_firmbirths'] + SZData['JC_EstabBirth'] + SZData['Job_Creation_Continuers']
SZData['JD'] = SZData['firmdeath_emp'] + SZData['JD_EstabDeath'] + SZData['Job_Destruction_Continuers']
# SIC and firm size

AgeData = pd.read_csv('/Users/allentran/Dropbox/Research/Retail/Data/bds_f_agesz_sic_release.csv')
AgeData = AgeData[['year2','sic1','fage4','fsize','emp','denom','estabs_entry','estabs_exit','d_flag']]
I = ~np.isnan(AgeData.emp)
AgeData = AgeData.loc[I,:]

Data = pd.read_csv('/Users/allentran/Dropbox/Research/Retail/Data/bds_f_szsic_release.csv')
Data = Data[['year2','Emp','sic1','fsize','Net_Job_Creation','Job_Creation','Job_Creation_Births',
'Job_Creation_Continuers','Job_Destruction','Job_Destruction_Deaths','Job_Destruction_Continuers','firmdeath_emp','d_flag',]]
I = Data.d_flag == 0
Data = Data.loc[I,:]
Data = Data.fillna(value=0)

JC_firmbirths = AgeData[AgeData.fage4 == 'a) 0'][['year2','sic1','fsize','emp']]
JC_firmbirths = JC_firmbirths.rename(columns={'emp':'JC_firmbirths'})

AllSizeData = JC_firmbirths.merge(Data,on=['sic1','fsize','year2'])



AllSizeData['JC_EstabBirth'] = AllSizeData['Job_Creation_Births'] - AllSizeData['JC_firmbirths']
AllSizeData['JD_EstabDeath'] = AllSizeData['Job_Destruction_Deaths'] - AllSizeData['firmdeath_emp']
AllSizeData['JC'] = AllSizeData['JC_firmbirths'] + AllSizeData['JC_EstabBirth'] + AllSizeData['Job_Creation_Continuers']
AllSizeData['JD'] = AllSizeData['firmdeath_emp'] + AllSizeData['JD_EstabDeath'] + AllSizeData['Job_Destruction_Continuers']

R = AllSizeData['sic1'] == 52
RetailSizeData = AllSizeData.loc[R,:]
M = AllSizeData['sic1'] == 20
ManSizeData = AllSizeData.loc[R,:]

# Job Creation Charts

FigStr = '/Users/allentran/Dropbox/Research/Retail/Figures/JC_'
Counter = 0
almost_black = '#626262'

def savefig(fig,FigStr,Counter):
	fig.savefig(FigStr+str(Counter)+'.pdf', format='pdf')
	Counter += 1
	return Counter

fig,ax = plt.subplots()
ax.set_xlabel("Job Creation - Firm Births")
plt.plot(RetailData.year2,AllData.JC_firmbirths/AllData.JC,label = 'All')
plt.plot(RetailData.year2,RetailData.JC_firmbirths/RetailData.JC,label = 'Retail')
plt.plot(RetailData.year2,ManData.JC_firmbirths/ManData.JC,label = 'Manufacturing')
ax.legend(frameon=False)
ax.set_ylabel('Fraction of job creation')

# Change the labels to the off-black
ax.xaxis.label.set_color(almost_black)
ax.yaxis.label.set_color(almost_black)
Counter = savefig(fig,FigStr,Counter)

fig1,ax1 = plt.subplots()
ax1.set_xlabel("Job Creation - Estab Births")
plt.plot(RetailData.year2,AllData.JC_EstabBirth/AllData.JC,label = 'All')
plt.plot(RetailData.year2,RetailData.JC_EstabBirth/RetailData.JC,label = 'Retail')
plt.plot(RetailData.year2,ManData.JC_EstabBirth/ManData.JC,label = 'Manufacturing')
ax1.legend(frameon=False)
ax1.set_ylabel('Fraction of job creation')
Counter = savefig(fig1,FigStr,Counter)

fig2,ax2 = plt.subplots()
ax2.set_xlabel("Job Creation - Continuers")
plt.plot(RetailData.year2,AllData.job_creation_continuers/AllData.JC,label = 'All')
plt.plot(RetailData.year2,RetailData.job_creation_continuers/RetailData.JC,label = 'Retail')
plt.plot(RetailData.year2,ManData.job_creation_continuers/ManData.JC,label = 'Manufacturing')
ax2.legend(frameon=False)
ax2.set_ylabel('Fraction of job creation')
Counter = savefig(fig2,FigStr,Counter)

fig6,ax6 = plt.subplots()
ax6.set_xlabel("Job Creation by Firm Size - Firm Births")
for ii,fsize in enumerate(np.unique(RetailSizeData.fsize)):
	I = SZData.fsize == fsize
	SubData = SZData.loc[I,:]
	plt.plot(SubData.year2,SubData.JC_firmbirths/SubData.JC,label = FixSizeStrings(fsize),color=Colors[ii])
ax6.legend(frameon=False)
ax6.set_ylabel('Fraction of job creation')
Counter = savefig(fig6,FigStr,Counter)

fig7,ax7 = plt.subplots()
ax7.set_xlabel("Job Creation by Firm Size - Estab Births")
for ii,fsize in enumerate(np.unique(RetailSizeData.fsize)):
	I = SZData.fsize == fsize
	SubData = SZData.loc[I,:]
	plt.plot(SubData.year2,SubData.JC_EstabBirth/SubData.JC,label = FixSizeStrings(fsize),color=Colors[ii])
ax7.legend(frameon=False)
ax7.set_ylabel('Fraction of job creation')
Counter = savefig(fig7,FigStr,Counter)

fig8,ax8 = plt.subplots()
ax8.set_xlabel("Job Creation by Firm Size - Continuers")
for ii,fsize in enumerate(np.unique(RetailSizeData.fsize)):
	I = SZData.fsize == fsize
	SubData = SZData.loc[I,:]
	plt.plot(SubData.year2,SubData.Job_Creation_Continuers/SubData.JC,label = FixSizeStrings(fsize),color=Colors[ii])
ax8.legend(frameon=False)
ax8.set_ylabel('Fraction of job creation')
Counter = savefig(fig8,FigStr,Counter)

fig9,ax9 = plt.subplots()
ax9.set_xlabel("Retail Job Creation - Firm Births")
for ii,fsize in enumerate(np.unique(RetailSizeData.fsize)):
	I = (RetailSizeData.fsize == fsize) & (RetailSizeData['year2']>1985)
	SubData = RetailSizeData.loc[I,:]
	plt.plot(SubData.year2,SubData.JC_firmbirths/SubData.JC,label = FixSizeStrings(fsize),color=Colors[ii])
ax9.legend(frameon=False)
ax9.set_ylabel('Fraction of job creation')
Counter = savefig(fig9,FigStr,Counter)

fig4,ax4 = plt.subplots()
ax4.set_xlabel("Retail Job Creation - Estab Births")
for ii,fsize in enumerate(np.unique(RetailSizeData.fsize)):
	I = (RetailSizeData.fsize == fsize) & (RetailSizeData['year2']>1985)
	SubData = RetailSizeData.loc[I,:]
	plt.plot(SubData.year2,SubData.JC_EstabBirth/SubData.JC,label = FixSizeStrings(fsize),color=Colors[ii])
ax4.legend(frameon=False)
ax4.set_ylabel('Fraction of job creation')
Counter = savefig(fig4,FigStr,Counter)

fig5,ax5 = plt.subplots()
ax5.set_xlabel("Retail Job Creation - Continuers")
for ii,fsize in enumerate(np.unique(RetailSizeData.fsize)):
	I = (RetailSizeData.fsize == fsize) & (RetailSizeData['year2']>1985)
	SubData = RetailSizeData.loc[I,:]
	plt.plot(SubData.year2,SubData.Job_Creation_Continuers/SubData.JC,label = FixSizeStrings(fsize),color=Colors[ii])
ax5.legend(frameon=False)
ax5.set_ylabel('Fraction of job creation')
Counter = savefig(fig5,FigStr,Counter)

fig9,ax9 = plt.subplots()
ax9.set_xlabel("Manufacturing Job Creation - Firm Births")
for ii,fsize in enumerate(np.unique(ManSizeData.fsize)):
	I = (ManSizeData.fsize == fsize) & (ManSizeData['year2']>1985)
	SubData = ManSizeData.loc[I,:]
	plt.plot(SubData.year2,SubData.JC_firmbirths/SubData.JC,label = FixSizeStrings(fsize),color=Colors[ii])
ax9.legend(frameon=False)
ax9.set_ylabel('Fraction of job creation')
Counter = savefig(fig9,FigStr,Counter)

fig10,ax10 = plt.subplots()
ax10.set_xlabel("Manufacturing Job Creation - Estab Births")
for ii,fsize in enumerate(np.unique(ManSizeData.fsize)):
	I = (ManSizeData.fsize == fsize) & (ManSizeData['year2']>1985)
	SubData = ManSizeData.loc[I,:]
	plt.plot(SubData.year2,SubData.JC_EstabBirth/SubData.JC,label = FixSizeStrings(fsize),color=Colors[ii])
ax10.legend(frameon=False)
ax10.set_ylabel('Fraction of job creation')
Counter = savefig(fig10,FigStr,Counter)

fig11,ax11 = plt.subplots()
ax11.set_xlabel("Manufacturing Job Creation - Continuers")
for ii,fsize in enumerate(np.unique(ManSizeData.fsize)):
	I = (ManSizeData.fsize == fsize) & (ManSizeData['year2']>1985)
	SubData = ManSizeData.loc[I,:]
	plt.plot(SubData.year2,SubData.Job_Creation_Continuers/SubData.JC,label = FixSizeStrings(fsize),color=Colors[ii])
ax11.legend(frameon=False)
ax11.set_ylabel('Fraction of job creation')
Counter = savefig(fig11,FigStr,Counter)

fig9,ax9 = plt.subplots()
ax9.set_xlabel("Retail Net Job Creation - Net Firm Births")
for ii,fsize in enumerate(np.unique(RetailSizeData.fsize)):
	I = (RetailSizeData.fsize == fsize) & (RetailSizeData['year2']>1985)
	SubData = RetailSizeData.loc[I,:]
	plt.plot(SubData.year2,SubData.JC_firmbirths - SubData.firmdeath_emp,label = FixSizeStrings(fsize),color=Colors[ii])
ax9.legend(frameon=False)
ax9.set_ylabel('Net Job Creation')
Counter = savefig(fig9,FigStr,Counter)

fig4,ax4 = plt.subplots()
ax4.set_xlabel("Retail Net Job Creation - Net Estab Births")
for ii,fsize in enumerate(np.unique(RetailSizeData.fsize)):
	I = (RetailSizeData.fsize == fsize) & (RetailSizeData['year2']>1985)
	SubData = RetailSizeData.loc[I,:]
	plt.plot(SubData.year2,SubData.JC_EstabBirth - SubData.JD_EstabDeath,label = FixSizeStrings(fsize),color=Colors[ii])
ax4.legend(frameon=False)
ax4.set_ylabel('Net Job Creation')
Counter = savefig(fig4,FigStr,Counter)

fig5,ax5 = plt.subplots()
ax5.set_xlabel("Retail Net Job Creation - Continuers")
for ii,fsize in enumerate(np.unique(RetailSizeData.fsize)):
	I = (RetailSizeData.fsize == fsize) & (RetailSizeData['year2']>1985)
	SubData = RetailSizeData.loc[I,:]
	plt.plot(SubData.year2,SubData.Job_Creation_Continuers - SubData.Job_Destruction_Continuers,label = FixSizeStrings(fsize),color=Colors[ii])
ax5.legend(frameon=False)
ax5.set_ylabel('Net Job Creation')
Counter = savefig(fig5,FigStr,Counter)

fig9,ax9 = plt.subplots()
ax9.set_xlabel("Net Job Creation - Net Firm Births")
for ii,fsize in enumerate(np.unique(RetailSizeData.fsize)):
	I = (SZData.fsize == fsize) & (SZData['year2']>1985)
	SubData = SZData.loc[I,:]
	plt.plot(SubData.year2,SubData.JC_firmbirths - SubData.firmdeath_emp,label = FixSizeStrings(fsize),color=Colors[ii])
ax9.legend(frameon=False)
ax9.set_ylabel('Net Job Creation')
Counter = savefig(fig9,FigStr,Counter)

fig4,ax4 = plt.subplots()
ax4.set_xlabel("Net Job Creation - Net Estab Births")
for ii,fsize in enumerate(np.unique(RetailSizeData.fsize)):
	I = (SZData.fsize == fsize) & (SZData['year2']>1985)
	SubData = SZData.loc[I,:]
	plt.plot(SubData.year2,SubData.JC_EstabBirth - SubData.JD_EstabDeath,label = FixSizeStrings(fsize),color=Colors[ii])
ax4.legend(frameon=False)
ax4.set_ylabel('Net Job Creation')
Counter = savefig(fig4,FigStr,Counter)

fig5,ax5 = plt.subplots()
ax5.set_xlabel("Net Job Creation - Continuers")
for ii,fsize in enumerate(np.unique(RetailSizeData.fsize)):
	I = (SZData.fsize == fsize) & (SZData['year2']>1985)
	SubData = SZData.loc[I,:]
	plt.plot(SubData.year2,SubData.Job_Creation_Continuers - SubData.Job_Destruction_Continuers,label = FixSizeStrings(fsize),color=Colors[ii])
ax5.legend(frameon=False)
ax5.set_ylabel('Net Job Creation')
Counter = savefig(fig5,FigStr,Counter)

# Job Destruction Charts

FigStr = '/Users/allentran/Dropbox/Research/Retail/Figures/JD_'
Counter = 0

fig,ax = plt.subplots()
ax.set_xlabel("Job Destruction - Firm Deaths")
plt.plot(RetailData.year2,AllData.firmdeath_emp/AllData.JD,label = 'All')
plt.plot(RetailData.year2,RetailData.firmdeath_emp/RetailData.JD,label = 'Retail')
plt.plot(RetailData.year2,ManData.firmdeath_emp/ManData.JD,label = 'Manufacturing')
ax.legend(frameon=False)
ax.set_ylabel('Fraction of job destruction')
Counter = savefig(fig,FigStr,Counter)

fig1,ax1 = plt.subplots()
ax1.set_xlabel("Job Destruction - Estab Deaths")
plt.plot(RetailData.year2,AllData.JD_EstabDeath/AllData.JD,label = 'All')
plt.plot(RetailData.year2,RetailData.JD_EstabDeath/RetailData.JD,label = 'Retail')
plt.plot(RetailData.year2,ManData.JD_EstabDeath/ManData.JD,label = 'Manufacturing')
ax1.legend(frameon=False)
ax1.set_ylabel('Fraction of job destruction')
Counter = savefig(fig1,FigStr,Counter)

fig2,ax2 = plt.subplots()
ax2.set_xlabel("Job Destruction - Continuers")
plt.plot(RetailData.year2,AllData.job_destruction_continuers/AllData.JD,label = 'All')
plt.plot(RetailData.year2,RetailData.job_destruction_continuers/RetailData.JD,label = 'Retail')
plt.plot(RetailData.year2,ManData.job_destruction_continuers/ManData.JD,label = 'Manufacturing')
ax2.legend(frameon=False)
ax2.set_ylabel('Fraction of job destruction')
Counter = savefig(fig2,FigStr,Counter)

fig6,ax6 = plt.subplots()
ax6.set_xlabel("Job Destruction by Firm Size - Firm Deaths")
for ii,fsize in enumerate(np.unique(RetailSizeData.fsize)):
	I = SZData.fsize == fsize
	SubData = SZData.loc[I,:]
	plt.plot(SubData.year2,SubData.firmdeath_emp/SubData.JD,label = FixSizeStrings(fsize),color=Colors[ii])
ax6.legend(frameon=False)
ax6.set_ylabel('Fraction of job destruction')
Counter = savefig(fig6,FigStr,Counter)

fig7,ax7 = plt.subplots()
ax7.set_xlabel("Job Destruction by Firm Size - Estab Deaths")
for ii,fsize in enumerate(np.unique(RetailSizeData.fsize)):
	I = SZData.fsize == fsize
	SubData = SZData.loc[I,:]
	plt.plot(SubData.year2,SubData.JD_EstabDeath/SubData.JD,label = FixSizeStrings(fsize),color=Colors[ii])
ax7.legend(frameon=False)
ax7.set_ylabel('Fraction of job destruction')
Counter = savefig(fig7,FigStr,Counter)

fig8,ax8 = plt.subplots()
ax8.set_xlabel("Job Destruction by Firm Size - Continuers")
for ii,fsize in enumerate(np.unique(RetailSizeData.fsize)):
	I = SZData.fsize == fsize
	SubData = SZData.loc[I,:]
	plt.plot(SubData.year2,SubData.Job_Destruction_Continuers/SubData.JD,label = FixSizeStrings(fsize),color=Colors[ii])
ax8.legend(frameon=False)
ax8.set_ylabel('Fraction of job destruction')
Counter = savefig(fig8,FigStr,Counter)

fig9,ax9 = plt.subplots()
ax9.set_xlabel("Retail Job Destruction - Firm Deaths")
for ii,fsize in enumerate(np.unique(RetailSizeData.fsize)):
	I = (RetailSizeData.fsize == fsize) & (RetailSizeData['year2']>1985)
	SubData = RetailSizeData.loc[I,:]
	plt.plot(SubData.year2,SubData.firmdeath_emp/SubData.JD,label = FixSizeStrings(fsize),color=Colors[ii])
ax9.legend(frameon=False)
ax9.set_ylabel('Fraction of job destruction')
Counter = savefig(fig9,FigStr,Counter)


fig4,ax4 = plt.subplots(1)
ax4.set_xlabel("Retail Job Destruction - Estab Deaths")
for ii,fsize in enumerate(np.unique(RetailSizeData.fsize)):
	I = (RetailSizeData.fsize == fsize) & (RetailSizeData['year2']>1985)
	SubData = RetailSizeData.loc[I,:]
	plt.plot(SubData.year2,SubData.JD_EstabDeath/SubData.JD,label = FixSizeStrings(fsize),color=Colors[ii])
ax4.legend(frameon=False)
ax4.set_ylabel('Fraction of job destruction')
Counter = savefig(fig4,FigStr,Counter)

fig5,ax5 = plt.subplots()
ax5.set_xlabel("Retail Job Destruction - Continuers")
for ii,fsize in enumerate(np.unique(RetailSizeData.fsize)):
	I = (RetailSizeData.fsize == fsize) & (RetailSizeData['year2']>1985)
	SubData = RetailSizeData.loc[I,:]
	plt.plot(SubData.year2,SubData.Job_Destruction_Continuers/SubData.JD,label = FixSizeStrings(fsize),color=Colors[ii])
ax5.legend(frameon=False)
ax5.set_ylabel('Fraction of job destruction')
Counter = savefig(fig5,FigStr,Counter)

fig9,ax9 = plt.subplots()
ax9.set_xlabel("Manufacturing Job Destruction - Firm Deaths")
for ii,fsize in enumerate(np.unique(ManSizeData.fsize)):
	I = (ManSizeData.fsize == fsize) & (ManSizeData['year2']>1985)
	SubData = ManSizeData.loc[I,:]
	plt.plot(SubData.year2,SubData.firmdeath_emp/SubData.JD,label = FixSizeStrings(fsize),color=Colors[ii])
ax9.legend(frameon=False)
ax9.set_ylabel('Fraction of job destruction')
Counter = savefig(fig9,FigStr,Counter)

fig10,ax10 = plt.subplots(1)
ax10.set_xlabel("Manufacturing Job Destruction - Estab Deaths")
for ii,fsize in enumerate(np.unique(ManSizeData.fsize)):
	I = (ManSizeData.fsize == fsize) & (ManSizeData['year2']>1985)
	SubData = ManSizeData.loc[I,:]
	plt.plot(SubData.year2,SubData.JD_EstabDeath/SubData.JD,label = FixSizeStrings(fsize),color=Colors[ii])
ax10.legend(frameon=False)
ax10.set_ylabel('Fraction of job destruction')
Counter = savefig(fig10,FigStr,Counter)

fig11,ax11 = plt.subplots()
ax11.set_xlabel("Manufacturing Job Destruction - Continuers")
for ii,fsize in enumerate(np.unique(ManSizeData.fsize)):
	I = (ManSizeData.fsize == fsize) & (ManSizeData['year2']>1985)
	SubData = ManSizeData.loc[I,:]
	plt.plot(SubData.year2,SubData.Job_Destruction_Continuers/SubData.JD,label = FixSizeStrings(fsize),color=Colors[ii])
ax11.legend(frameon=False)
ax11.set_ylabel('Fraction of job destruction')
Counter = savefig(fig11,FigStr,Counter)





