# Twitter API v2 data dictionary

## Tweet

Tweets are the basic building block of all things Twitter. The Tweet object has a long list of ‘root-level’ fields, such as id, text, and created_at. Tweet objects are also the ‘parent’ object to several child objects including user, media, poll, and place. Use the field parameter tweet.fields when requesting these root-level fields on the Tweet object.

The Tweet object that can be found and expanded in the user resource. Additional Tweets related to the requested Tweet can also be found and expanded in the Tweet resource. The object is available for expansion with ?expansions=pinned_tweet_id in the user resource or ?expansions=referenced_tweets.id in the Tweet resource to get the object with only default fields. Use the expansion with the field parameter: tweet.fields when requesting additional fields to complete the object.



## User
> Link: https://developer.x.com/en/docs/x-api/data-dictionary/object-model/user

The user object contains Twitter user account metadata describing the referenced user. The user object is the primary object returned in the users lookup endpoint. When requesting additional user fields on this endpoint, simply use the fields parameter `user.fields`.

The user object can also be found as a child object and expanded in the Tweet object. The object is available for expansion with `?expansions=author_id` or `?expansions=in_reply_to_user_id` to get the condensed object with only default fields. Use the expansion with the field parameter: `user.fields` when requesting additional fields to complete the object.

### Retrieving a user object

**Sample Request**

In the following request, we are requesting fields for the user on the [users lookup](https://developer.x.com/en/docs/x-api/users/lookup/introduction) endpoint. Be sure to replace `$BEARER_TOKEN` with your own generated [Bearer Token](https://developer.x.com/en/docs/authentication/oauth-2-0/bearer-tokens).

```
curl --request GET 'https://api.x.com/2/users?ids=2244994945&user.fields=created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,url,username,verified,withheld&expansions=pinned_tweet_id' --header 'Authorization: Bearer $BEARER_TOKEN'
```

**Sample Response**

```
{
    "data": [
        {
            "id": "2244994945",
            "name": "Twitter Dev",
            "username": "TwitterDev",
            "location": "127.0.0.1",
            "entities": {
                "url": {
                    "urls": [
                        {
                            "start": 0,
                            "end": 23,
                            "url": "https://t.co/3ZX3TNiZCY",
                            "expanded_url": "/content/developer-twitter/en/community",
                            "display_url": "developer.twitter.com/en/community"
                        }
                    ]
                },
                "description": {
                    "hashtags": [
                        {
                            "start": 23,
                            "end": 30,
                            "tag": "DevRel"
                        },
                        {
                            "start": 113,
                            "end": 130,
                            "tag": "BlackLivesMatter"
                        }
                    ]
                }
            },
            "verified": true,
            "description": "The voice of Twitter's #DevRel team, and your official source for updates, news, & events about Twitter's API. \n\n#BlackLivesMatter",
            "url": "https://t.co/3ZX3TNiZCY",
            "profile_image_url": "https://pbs.twimg.com/profile_images/1267175364003901441/tBZNFAgA_normal.jpg",
            "protected": false,
            "pinned_tweet_id": "1255542774432063488",
            "created_at": "2013-12-14T04:35:55.000Z"
        }
    ],
    "includes": {
        "tweets": [
            {
                "id": "1255542774432063488",
                "text": "During these unprecedented times, what’s happening on Twitter can help the world better understand &amp; respond to the pandemic. \n\nWe're launching a free COVID-19 stream endpoint so qualified devs &amp; researchers can study the public conversation in real-time. https://t.co/BPqMcQzhId"
            }
        ]
    }
}
```