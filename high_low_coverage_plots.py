import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import ast

freebayesGraphiteTotals = {'freebayes': [], 'graphite': [], 'classification': []}
freebayesGraphiteCounts = {'freebayes': [], 'graphite': []}
f = open('data/freebayes-graphite-counts.txt')
for line in f:
    tmpList = ast.literal_eval(line)
    fbSum = sum(tmpList[0])
    gSum = sum(tmpList[1])
    # if fbSum >= 20 and gSum >= 20:
        # continue
    classification = 0 # gSum and
    if gSum > 20 and fbSum >20:
        classification = 1
    elif gSum >= 20 and fbSum <= 20:
        classification = 2
    elif gSum <= 20 and fbSum >= 20:
        classification = 3
    freebayesGraphiteCounts['freebayes'].append(tmpList[0])
    freebayesGraphiteCounts['graphite'].append(tmpList[1])
    freebayesGraphiteTotals['freebayes'].append(fbSum)
    freebayesGraphiteTotals['graphite'].append(gSum)
    freebayesGraphiteTotals['classification'].append(classification)

freebayesGraphiteDF = pd.DataFrame({'freebayes':freebayesGraphiteTotals['freebayes'], 'graphite': freebayesGraphiteTotals['graphite'], 'classification': freebayesGraphiteTotals['classification']})
# sns.lmplot(x='freebayes', y='graphite', data=freebayesGraphiteDF, hue='classification')
# freebayesGraphiteDF.plot(x='freebayes', y='graphite', kind='scatter')



def plotCoverage(picFileName, graphiteLowCoverage, freebayesGraphiteDF, percentile):

    freebayesQuantile = freebayesGraphiteDF.freebayes.quantile(percentile)
    graphiteQuantile = freebayesGraphiteDF.graphite.quantile(percentile)
    maxQuantile = max(freebayesQuantile, graphiteQuantile)

    noneAgree = freebayesGraphiteDF.loc[freebayesGraphiteDF['classification'] == 0]
    bothAgree = freebayesGraphiteDF.loc[freebayesGraphiteDF['classification'] == 1]
    onlyGraphiteAgree = freebayesGraphiteDF.loc[freebayesGraphiteDF['classification'] == 2]
    onlyFreebayesAgree = freebayesGraphiteDF.loc[freebayesGraphiteDF['classification'] == 3]

    print("quantile: " + str(maxQuantile))
    print("none agree: " + str(len(noneAgree.index)))
    print("both agree: " + str(len(bothAgree.index)))
    print("freebayes agree: " + str(len(onlyFreebayesAgree.index)))
    print("graphite agree: " + str(len(onlyGraphiteAgree.index)))

    dotSize = 60

    plt.scatter(noneAgree['freebayes'], noneAgree['graphite'], alpha=0.4, s=dotSize, c='gray')
    plt.scatter(bothAgree['freebayes'], bothAgree['graphite'], alpha=0.4, s=dotSize, c='gray')
    if graphiteLowCoverage:
        plt.scatter(onlyGraphiteAgree['freebayes'], onlyGraphiteAgree['graphite'], alpha=0.4, s=dotSize, c='gray')
        plt.scatter(onlyFreebayesAgree['freebayes'], onlyFreebayesAgree['graphite'], alpha=0.4, s=dotSize, c='mediumseagreen')
    else:
        plt.scatter(onlyFreebayesAgree['freebayes'], onlyFreebayesAgree['graphite'], alpha=0.4, s=dotSize, c='gray')
        plt.scatter(onlyGraphiteAgree['freebayes'], onlyGraphiteAgree['graphite'], alpha=0.4, s=dotSize, c='steelblue')

    # plt.figure(figsize=(4,4))
    plt.xlim(0, maxQuantile)
    plt.ylim(0, maxQuantile)
    plt.gca().set_aspect('equal', adjustable='box')
    # plt.show()
    plt.savefig(picFileName, dpi=(200))
    plt.cla()
    plt.clf()
    # print(freebayesGraphiteDF)
    # sns.lmplot(x='Freebayes', y='Graphite', data=freebayesGraphiteTotals)

plotCoverage("GraphiteLowCoverage.png", True, freebayesGraphiteDF, 0.90)
plotCoverage("GraphiteHighCoverage.png", False, freebayesGraphiteDF, 0.90)
