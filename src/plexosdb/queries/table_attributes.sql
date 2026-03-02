SELECT o.name AS name, c.name AS class, a.name AS attribute, ad.value, a.attribute_id as attribute_enum_id, a.class_id as base_class_id
FROM t_attribute_data ad
LEFT JOIN t_attribute a ON ad.attribute_id = a.attribute_id
LEFT JOIN t_object o ON ad.object_id = o.object_id
LEFT JOIN t_class c ON a.class_id = c.class_id
${where_clause}
