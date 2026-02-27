SELECT c.name AS class_name, cat.category_id, cat.name AS category, cat.description
FROM t_category cat
LEFT JOIN t_class c ON cat.class_id = c.class_id
${where_clause}
