SELECT o.name AS object, a.name AS attribute_name, ad.value, ad.source
FROM t_attribute_data ad
LEFT JOIN t_attribute a ON ad.attribute_id = a.attribute_id
LEFT JOIN t_object o ON ad.object_id = o.object_id
${where_clause}
