"""
data = pandas.Dataframe()
"""


# SELECT * FROM data;
select_all = data

# SELECT * FROM data LIMIT 10;
select_limit = data[: 10]

# SELECT id FROM data;
select_id = data[["id"]]

# SELECT COUNT(id) FROM data;
select_count = data["id"].count()

# SELECT * FROM data WHERE id<1000 AND age>30;
select_betweet = data[(data["id"] < 1000) & (data["age"] > 30)]

# SELECT id,COUNT(DISTINCT order_id) FROM table1 GROUP BY id;
select_group_by = data.groupby(by=["id"]).agg({"order_id": [("order_id_count", "nunique")]})

# SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id;
select_convert = pd.merge(table1, table2, on="id", how="inner")

# SELECT * FROM table1 UNION SELECT * FROM table2;
select_union = pd.concat([table1, table2], axis=0, ignore_index=True).drop_duplicates().reset_index()

# DELETE FROM table1 WHERE id=10;
delete_id = table1.drop(table1[table1["id"]==10].index).reset_index()

# ALTER TABLE table1 DROP COLUMN column_name  (column_name=id);
alter_row = data.drop("id", axis=1)