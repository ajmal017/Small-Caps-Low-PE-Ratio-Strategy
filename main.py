### PRODUCT INFORMATION --------------------------------------------------------------------------------
# Copyright InnoQuantivity.com, granted to the public domain.
# Use entirely at your own risk.
# This algorithm contains open source code from other sources and no claim is being made to such code.
# Do not remove this copyright notice.
### ----------------------------------------------------------------------------------------------------

from SmallCapsLowPERatioUniverseSelection import SmallCapsLowPERatioUniverseSelectionModel
from LongOnlyConstantAlphaCreation import LongOnlyConstantAlphaCreationModel
from CustomEqualWeightingPortfolioConstruction import CustomEqualWeightingPortfolioConstructionModel

class LongOnlySmallCapsLowPERatioFrameworkAlgorithm(QCAlgorithmFramework):
    
    '''
    Trading Logic:
        This algorithm buys at the start of every year Small Caps with low P/E Ratio
    Universe: Dynamically selects stocks at the start of each year based on:
        - Price above $5
        - Small Caps (Market Cap between $300 million and $2 billion)
        - Then select stocks in the 1st percentile of Price To Earnings Ratio (PE Ratio)
    Alpha: Constant creation of Up Insights every trading bar
    Portfolio: Equal Weighting (allocate equal amounts of portfolio % to each security)
        - To rebalance the portfolio periodically to ensure equal weighting, change the rebalancingParam below
    Execution: Immediate Execution with Market Orders
    Risk: Null
    '''

    def Initialize(self):
        
        ### user-defined inputs --------------------------------------------------------------

        self.SetStartDate(2015, 1, 1)   # set start date
        #self.SetEndDate(2019, 1, 4)     # set end date
        self.SetCash(100000)            # set strategy cash
        
        # True/False to enable/disable filtering by fundamental data
        filterFineData = True
        
        # rebalancing period (to enable rebalancing enter an integer for number of days, e.g. 1, 7, 30, 365)
        rebalancingParam = False
        
        ### -----------------------------------------------------------------------------------
        
        # set the brokerage model for slippage and fees
        self.SetBrokerageModel(AlphaStreamsBrokerageModel())
        
        # set requested data resolution and disable fill forward data
        self.UniverseSettings.Resolution = Resolution.Daily
        self.UniverseSettings.FillForward = False
        
        # select modules
        self.SetUniverseSelection(SmallCapsLowPERatioUniverseSelectionModel(filterFineData = filterFineData))
        self.SetAlpha(LongOnlyConstantAlphaCreationModel())
        self.SetPortfolioConstruction(CustomEqualWeightingPortfolioConstructionModel(rebalancingParam = rebalancingParam))
        self.SetExecution(ImmediateExecutionModel())
        self.SetRiskManagement(NullRiskManagementModel())