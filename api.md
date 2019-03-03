# Adding to the Database

Use PUT requests directed at `api/add`. The content should be a JSON string in the format shown below:

```
{
	"source_type" = "twitter",
	"url" = "https://link.com/somestuff",
	"disaster_type = "flood",
	"date_created" = "2018-05-19",
	"location_name" = "San Diego, California",
	"country" = "USA",
	"geo_location" = [16.33432, 20.32435]
	"disaster_severity" = "medium",
	"tags" = "disaster,people"
}
```

The first three parameters -- `source_type`, `url`, and `disaster_type` are required. All others are optional.