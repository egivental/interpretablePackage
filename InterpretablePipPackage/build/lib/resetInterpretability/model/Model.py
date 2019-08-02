
class Model():
    """
    This is the base class for all implemented interpretable models.  New interpretability
    algorithms should extend this class and implement the methods below.  The methods and names are
    based on the scikit-learn approach.
    """

    def __init__(self):
        pass

    def fit(self, X, Y):
        """
        Trains the model based on the given array X of training samples and the array Y of training
        labels.  Returns the trained model object.
        """
        raise NotImplementedError("fit(X,Y) in Model is not implemented")

    def predict(self, X):
        """
        Runs the given X data samples through the model and returns an array of the predictions.
        """
        raise NotImplementedError("predict(X) in Model is not implemented")

    def get_name(self):
        """
        Returns the name for the algorithm.  This must be a unique name, so it is suggested that
        this name is simply <firstauthor>, i.e. the last name of the first author of the associated
        paper.  If there are mutliple algorithms by the same author(s), a suggested modification is
        <firstauthor-algname>.  This name will appear in the resulting CSVs and graphs created when
        performing benchmarks and analysis over multiple models.
        """
        return self.name
