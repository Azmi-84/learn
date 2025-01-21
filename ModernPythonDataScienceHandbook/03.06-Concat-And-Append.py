import marimo

__generated_with = "0.10.15"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Combining Datasets: concat and append
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Some of the most interesting studies of data come from combining different data sources.
        These operations can involve anything from very straightforward concatenation of two different datasets to more complicated database-style joins and merges that correctly handle any overlaps between the datasets.
        `Series` and ``DataFrame``s are built with this type of operation in mind, and Pandas includes functions and methods that make this sort of data wrangling fast and straightforward.

        Here we'll take a look at simple concatenation of `Series` and ``DataFrame``s with the `pd.concat` function; later we'll dive into more sophisticated in-memory merges and joins implemented in Pandas.

        We begin with the standard imports:
        """
    )
    return


@app.cell
def _():
    import pandas as pd
    import numpy as np
    return np, pd


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        For convenience, we'll define this function, which creates a `DataFrame` of a particular form that will be useful in the following examples:
        """
    )
    return


@app.cell
def _(pd):
    def make_df(cols, ind):
        """Quickly make a DataFrame"""
        data = {c: [str(c) + str(i) for i in ind]
                for c in cols}
        return pd.DataFrame(data, ind)

    # example DataFrame
    make_df('ABC', range(3))
    return (make_df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        In addition, we'll create a quick class that allows us to display multiple ``DataFrame``s side by side. The code makes use of the special `_repr_html_` method, which IPython/Jupyter uses to implement its rich object display:
        """
    )
    return


@app.cell
def _():
    class display(object):
        """Display HTML representation of multiple objects"""
        template = """<div style="float: left; padding: 10px;">
        <p style='font-family:"Courier New", Courier, monospace'>{0}</p>{1}
        </div>"""
        def __init__(self, *args):
            self.args = args
            
        def _repr_html_(self):
            return '\n'.join(self.template.format(a, eval(a)._repr_html_())
                             for a in self.args)
        
        def __repr__(self):
            return '\n\n'.join(a + '\n' + repr(eval(a))
                               for a in self.args)
    return (display,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        The use of this will become clearer as we continue our discussion in the following section.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Recall: Concatenation of NumPy Arrays

        Concatenation of `Series` and `DataFrame` objects behaves similarly to concatenation of NumPy arrays, which can be done via the `np.concatenate` function, as discussed in [The Basics of NumPy Arrays](02.02-The-Basics-Of-NumPy-Arrays.ipynb).
        Recall that with it, you can combine the contents of two or more arrays into a single array:
        """
    )
    return


@app.cell
def _(np):
    x = [1, 2, 3]
    y = [4, 5, 6]
    z = [7, 8, 9]
    np.concatenate([x, y, z])
    return x, y, z


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        The first argument is a list or tuple of arrays to concatenate.
        Additionally, in the case of multidimensional arrays, it takes an `axis` keyword that allows you to specify the axis along which the result will be concatenated:
        """
    )
    return


@app.cell
def _(np):
    x_1 = [[1, 2], [3, 4]]
    np.concatenate([x_1, x_1], axis=1)
    return (x_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Simple Concatenation with pd.concat
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        The `pd.concat` function provides a similar syntax to `np.concatenate` but contains a number of options that we'll discuss momentarily:

        ```python
        # Signature in Pandas v1.3.5
        pd.concat(objs, axis=0, join='outer', ignore_index=False, keys=None,
                  levels=None, names=None, verify_integrity=False,
                  sort=False, copy=True)
        ```

        `pd.concat` can be used for a simple concatenation of `Series` or `DataFrame` objects, just as `np.concatenate` can be used for simple concatenations of arrays:
        """
    )
    return


@app.cell
def _(pd):
    ser1 = pd.Series(['A', 'B', 'C'], index=[1, 2, 3])
    ser2 = pd.Series(['D', 'E', 'F'], index=[4, 5, 6])
    pd.concat([ser1, ser2])
    return ser1, ser2


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        It also works to concatenate higher-dimensional objects, such as ``DataFrame``s:
        """
    )
    return


@app.cell
def _(display, make_df):
    df1 = make_df('AB', [1, 2])
    df2 = make_df('AB', [3, 4])
    display('df1', 'df2', 'pd.concat([df1, df2])')
    return df1, df2


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        It's default behavior is to concatenate row-wise within the `DataFrame` (i.e., `axis=0`).
        Like `np.concatenate`, `pd.concat` allows specification of an axis along which concatenation will take place.
        Consider the following example:
        """
    )
    return


@app.cell
def _(display, make_df):
    df3 = make_df('AB', [0, 1])
    df4 = make_df('CD', [0, 1])
    display('df3', 'df4', "pd.concat([df3, df4], axis='columns')")
    return df3, df4


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        We could have equivalently specified ``axis=1``; here we've used the more intuitive ``axis='columns'``. 
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Duplicate Indices

        One important difference between `np.concatenate` and `pd.concat` is that Pandas concatenation *preserves indices*, even if the result will have duplicate indices!
        Consider this short example:
        """
    )
    return


@app.cell
def _(display, make_df):
    x_2 = make_df('AB', [0, 1])
    y_1 = make_df('AB', [2, 3])
    y_1.index = x_2.index
    display('x', 'y', 'pd.concat([x, y])')
    return x_2, y_1


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Notice the repeated indices in the result.
        While this is valid within ``DataFrame``s, the outcome is often undesirable.
        `pd.concat` gives us a few ways to handle it.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        #### Treating repeated indices as an error

        If you'd like to simply verify that the indices in the result of `pd.concat` do not overlap, you can include the `verify_integrity` flag.
        With this set to `True`, the concatenation will raise an exception if there are duplicate indices.
        Here is an example, where for clarity we'll catch and print the error message:
        """
    )
    return


@app.cell
def _(pd, x_2, y_1):
    try:
        pd.concat([x_2, y_1], verify_integrity=True)
    except ValueError as e:
        print('ValueError:', e)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        #### Ignoring the index

        Sometimes the index itself does not matter, and you would prefer it to simply be ignored.
        This option can be specified using the `ignore_index` flag.
        With this set to `True`, the concatenation will create a new integer index for the resulting `DataFrame`:
        """
    )
    return


@app.cell
def _(display):
    display('x', 'y', 'pd.concat([x, y], ignore_index=True)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        #### Adding MultiIndex keys

        Another option is to use the `keys` option to specify a label for the data sources; the result will be a hierarchically indexed series containing the data:
        """
    )
    return


@app.cell
def _(display):
    display('x', 'y', "pd.concat([x, y], keys=['x', 'y'])")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        We can use the tools discussed in [Hierarchical Indexing](03.05-Hierarchical-Indexing.ipynb) to transform this multiply indexed `DataFrame` into the representation we're interested in.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Concatenation with Joins

        In the short examples we just looked at, we were mainly concatenating ``DataFrame``s with shared column names.
        In practice, data from different sources might have different sets of column names, and `pd.concat` offers several options in this case.
        Consider the concatenation of the following two ``DataFrame``s, which have some (but not all!) columns in common:
        """
    )
    return


@app.cell
def _(display, make_df):
    df5 = make_df('ABC', [1, 2])
    df6 = make_df('BCD', [3, 4])
    display('df5', 'df6', 'pd.concat([df5, df6])')
    return df5, df6


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        The default behavior is to fill entries for which no data is available with NA values.
        To change this, we can adjust the `join` parameter of the `concat` function.
        By default, the join is a union of the input columns (`join='outer'`), but we can change this to an intersection of the columns using `join='inner'`:
        """
    )
    return


@app.cell
def _(display):
    display('df5', 'df6',
            "pd.concat([df5, df6], join='inner')")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Another useful pattern is to use the `reindex` method before concatenation for finer control over which columns are dropped:
        """
    )
    return


@app.cell
def _(df5, df6, pd):
    pd.concat([df5, df6.reindex(df5.columns, axis=1)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### The append Method

        Because direct array concatenation is so common, `Series` and `DataFrame` objects have an `append` method that can accomplish the same thing in fewer keystrokes.
        For example, in place of `pd.concat([df1, df2])`, you can use `df1.append(df2)`:
        """
    )
    return


@app.cell
def _(display):
    display('df1', 'df2', 'df1.append(df2)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Keep in mind that unlike the `append` and `extend` methods of Python lists, the `append` method in Pandas does not modify the original object; instead it creates a new object with the combined data.
        It also is not a very efficient method, because it involves creation of a new index *and* data buffer.
        Thus, if you plan to do multiple `append` operations, it is generally better to build a list of `DataFrame` objects and pass them all at once to the `concat` function.

        In the next chapter, we'll look at a more powerful approach to combining data from multiple sources: the database-style merges/joins implemented in `pd.merge`.
        For more information on `concat`, `append`, and related functionality, see the ["Merge, Join, Concatenate and Compare" section](http://pandas.pydata.org/pandas-docs/stable/merging.html) of the Pandas documentation.
        """
    )
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
