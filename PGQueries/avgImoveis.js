db.imoveis.aggregate(
  [
    { $match : { location_type : "Rent" } },
    { $unwind: "$location"},
    { $group: { _id: { $toLower:"$neighborhood"}, totalPrice: { $avg: "$price" }, coord_x: {$last:"$location"}, coord_y: {$first:"$location"} } },
    { $sort: {_id: 1}},
    { $out: "precomedio"}    
  ]
)