import pandas as pd

# create a sample DataFrame
data = {'Name': ['Alice', 'Bob', 'Charlie', 'Dave'], 'Age': [25, 30, 35, 40]}
df = pd.DataFrame(data)

# create a Styler object by calling the style attribute on the DataFrame
styler = df.style

# apply styling to the 'Age' column based on a condition
styler = styler.applymap(lambda x: 'color: red' if x > 30 else '', subset=['Age'])

# set the table styles to add borders
table_styles = [{'selector': 'table', 'props': [('border-collapse', 'collapse')]},
                {'selector': 'th, td', 'props': [('border', '1px solid black')]}]
styler.set_table_styles(table_styles)

# call the render method on the Styler object to get the HTML table
html_table = styler.render(index=False)

# print the HTML table
print(html_table)
