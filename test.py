import main as foo
import pandas as pd

x = pd.Series(['Agoobi', 'Agoobo'])
bar = foo.pickle_blobber(x)
print(bar)
