Pycrunch navigation
====================

This document intends to describe how to move around the different
elements and structures that Crunch exposes

We are going to use the `site` session variable previously described.
That will be our intermediary between Python and Crunch.


Catalogs
--------

Every collection of elements in Crunch is a Shoji Catalog. We
can quickly interact with the datasets Catalog by doing:

```python
site.datasets
```

Catalogs provide some methods to handle individual elements. Let's
say we want to interact with the Dataset named "US Elections 2016" we
could reference that particular Dataset by doing:

```python
my_dataset = site.datsets.by('name').get("US Elections 2016").entity
```

Now the variable `my_datasets` holds a reference to the Dataset
we need to interact with. Just like we interacted with the datasets
Catalog, we can do it with a given Dataset variables:

```python
my_dataset.variables
```

In order to visualize, for example, the data contents of our dataset 
we can make use of the table entity:

```python
my_dataset.table.data
```

Pycrunch also allows us to interact with data using Pandas. For
this we need to know the identifier of the dataset we are interacting
with. We can easily get it by doing:

```python
dataset_id = my_dataset.id
```

To access a Pandas Dataframe of the data:

```python
from pycrunch import pandaslib as crunchpandas
df = crunchpandas.dataframe_from_dataset(site, dataset_id)
```
