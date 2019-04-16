# Working with the model



1. Step 1 is to make directories for where the model goes

```python
import pickle
import os 
dest = os.path.join('movieclassifier', 'pkl_objects')
if not os.path.exists(dest):
  os.makedirs(dest)
  # create subdirectories in the project called movieclassifier and pkl_objects
```



2. 

