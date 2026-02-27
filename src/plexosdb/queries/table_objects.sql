SELECT c.name AS class_name, o.GUID, o.name, cat.name AS category, o.description
FROM t_object o
LEFT JOIN t_class c ON o.class_id = c.class_id
LEFT JOIN t_category cat ON o.category_id = cat.category_id
${where_clause}
