Examples
--------

#### Creating a Dataset

You need to provide a dictionary containing the basic body for the Dataset.

```python
ds_body = {
    'body': {
        'name': 'My first dataset'
        }
    }

my_dataset = site.datasets.create(ds_body)
```

#### Loading an existing Dataset

Here's how you can load an existing dataset.

```python
my_dataset = site.datasets.by('name').get('My Name').entity
```

#### Creating a variable

In this example we create a categorical variable. As for the Dataset you have to 
provide a dictionary with it's body.

```python
var_body = {
    'body': {
        'name': 'Gender',
        'alias': 'gender',
        'type': 'categorical',
        'categories': [
            {'id': 1, 'name': 'M', 'numeric_value': None, 'missing': False},
            {'id': 2, 'name': 'F', 'numeric_value': None, 'missing': False},
            {'id': -1, 'name': 'No Data', 'numeric_value': None, 'missing': True}
        ],
        'values': [1, 2, 2, 2, 2, 1, {'?': -1}]
    }
}

my_var = my_dataset.variables.create(var_body)
```

#### Loading an existing variable

```python
my_var = my_dataset.variables.by('alias').get('my_alias').entity
```

#### Change the variable's attributes

You can change any variable's attribute by providing them as keyword 
arguments in the *edit* method:

```python
my_var.edit(name="my new name", alias='gender_ng')
```

#### Adding a description

```python
my_var.edit(description='My awesome description')
```

#### Hiding variables in the UI

`Note` that variables are simply not presented in the UI but accessible in the API!


```python
my_var.edit(discarded=True)
```

#### Changing categories

Either provide a complete list of new categories like in the *gender* 
example above or if you want to change only the name of a category 
you can achieve that with:

```python
my_var.body.categories[0]['name'] = 'My new category'
my_var.edit(categories=var.body.categories)
```

## Ordering

#### Ordering variables

Ordering variables is as easy as rearranging the order of their 
respective URL's in the `ds.variables.hier.graph` list

```python
my_dataset.variables.hier.graph = [var2.self, var1.self]
```

#### Grouping variables

You can group variables in *topics* by providing a dictionary in that list. 
If we wanted to group `var1` and `var2` we can simply:

```python
group = {'My Aweseome Group': [var1.self, var2.self]}
my_dataset.variables.hier.graph = [group]
```
