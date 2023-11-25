import pusher

pusher_client = pusher.Pusher(
  app_id='1713738',
  key='722ee6ec40fa4eae21c0',
  secret='7a7bc8862cdc1f6ce7e6',
  cluster='ap2',
  ssl=True
)

pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world'})