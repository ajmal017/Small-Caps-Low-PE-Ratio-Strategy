from clr import AddReference
AddReference("System")
AddReference("QuantConnect.Common")
AddReference("QuantConnect.Indicators")
AddReference("QuantConnect.Algorithm.Framework")

from QuantConnect.Data.UniverseSelection import *
from Selection.FundamentalUniverseSelectionModel import FundamentalUniverseSelectionModel

import numpy as np

class SmallCapsLowPERatioUniverseSelectionModel(FundamentalUniverseSelectionModel):
    
    '''
    Description:
        This Universe model selects Small Cap stocks with low P/E Ratio (in the 1st percentile)
    Details:
        The important thing to understand here is the internal flow of the Universe module:
            1) SelectCoarse filters stocks with price above $5
            2) SelectFine further filters those stocks by fundamental data. In this case, we use Market Cap and P/E Ratio
    '''

    def __init__(self, 
                filterFineData = True,
                universeSettings = None,
                securityInitializer = None):
        
        super().__init__(filterFineData, universeSettings, securityInitializer)
        
        self.periodCheck = -1 # initialize a variable to check when the period changes

    def SelectCoarse(self, algorithm, coarse):
        
        ''' Coarse selection based on price and volume '''
        
        # this ensures the universe selection only runs once a year
        if algorithm.Time.year == self.periodCheck:
            return Universe.Unchanged
        self.periodCheck = algorithm.Time.year
        
        # securities must have fundamental data (to avoid ETFs)
        # securities must have last price above $5
        filterCoarse = [x for x in coarse if x.HasFundamentalData and x.Price > 5]
        algorithm.Log('stocks with fundamental data and price above 5: ' + str(len(filterCoarse)))
        
        coarseSelection = [x.Symbol for x in filterCoarse]
        
        # return coarseSelection symbols ready for fundamental data filtering below
        return coarseSelection
        
    def SelectFine(self, algorithm, fine):
     
        ''' Fine selection based on fundamental data '''
        
        # select small caps only (market cap between $300 million and $2 billion)
        filterFine = [x for x in fine if 3e8 < x.MarketCap < 2e9 and x.ValuationRatios.PERatio > 0]
        algorithm.Log('total number of small caps: ' + str(len(filterFine)))
        
        # now calculate the PE Ratio 1st percentile
        peRatios = [x.ValuationRatios.PERatio for x in filterFine]
        lowestPERatioPercentile = np.percentile(peRatios, 1)
        
        # filter stocks in the 1st PE Ratio percentile
        lowestPERatio = list(filter(lambda x: x.ValuationRatios.PERatio <= lowestPERatioPercentile, filterFine))
        algorithm.Log('small caps in the 1st PE Ratio percentile: ' + str(len(lowestPERatio)))
        
        for x in lowestPERatio:
            algorithm.Log('stock: ' + str(x.Symbol.Value)
            + ', current PE Ratio: ' + str(x.ValuationRatios.PERatio))
        
        fineSelection = [x.Symbol for x in lowestPERatio]
         
        # return fineSelection ready for Alpha module
        return fineSelection