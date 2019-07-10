import asyncio
import re

import janus
import pytest
from nio import (
    DeviceList,
    DeviceOneTimeKeyCount,
    LoginResponse,
    RoomEncryptionEvent,
    RoomInfo,
    RoomMemberEvent,
    Rooms,
    RoomSummary,
    SyncResponse,
    Timeline,
)

from pantalaimon.client import PanClient
from pantalaimon.config import ServerConfig
from pantalaimon.store import PanStore

TEST_ROOM_ID = "!SVkFJHzfwvuaIEawgC:localhost"
TEST_ROOM2 = "!testroom:localhost"

ALICE_ID = "@alice:example.org"


@pytest.fixture
async def client(tmpdir, loop):
    store = PanStore(tmpdir)
    queue = janus.Queue(loop=loop)
    conf = ServerConfig("example", "https://exapmle.org")
    conf.history_fetch_delay = 0.1

    store.save_server_user("example", "@example:example.org")

    pan_client = PanClient(
        "example",
        store,
        conf,
        "https://example.org",
        queue.async_q,
        "@example:example.org",
        "DEVICEID",
        tmpdir
    )

    yield pan_client

    await pan_client.close()


class TestClass(object):
    @property
    def login_response(self):
        return LoginResponse.from_dict(
            {
                "access_token": "abc123",
                "device_id": "DEVICEID",
                "home_server": "example.org",
                "user_id": "@example:example.org"
            }
        )

    @property
    def initial_sync_response(self):
        return {
            "device_one_time_keys_count": {},
            "next_batch": "s526_47314_0_7_1_1_1_11444_1",
            "device_lists": {
                "changed": [
                    "@example:example.org"
                ],
                "left": []
            },

            "rooms": {
                "invite": {},
                "join": {
                    "!SVkFJHzfwvuaIEawgC:localhost": {
                        "account_data": {
                            "events": []
                        },
                        "ephemeral": {
                            "events": []
                        },
                        "state": {
                            "events": [
                                {
                                    "content": {
                                        "avatar_url": None,
                                        "displayname": "example",
                                        "membership": "join"
                                    },
                                    "event_id": "$151800140517rfvjc:localhost",
                                    "membership": "join",
                                    "origin_server_ts": 1518001405556,
                                    "sender": "@example:localhost",
                                    "state_key": "@example:localhost",
                                    "type": "m.room.member",
                                    "unsigned": {
                                        "age": 2970366338,
                                        "replaces_state": "$151800111315tsynI:localhost"
                                    }
                                },
                                {
                                    "content": {
                                        "history_visibility": "shared"
                                    },
                                    "event_id": "$15139375515VaJEY:localhost",
                                    "origin_server_ts": 1513937551613,
                                    "sender": "@example:localhost",
                                    "state_key": "",
                                    "type": "m.room.history_visibility",
                                    "unsigned": {
                                        "age": 7034220281
                                    }
                                },
                                {
                                    "content": {
                                        "creator": "@example:localhost"
                                    },
                                    "event_id": "$15139375510KUZHi:localhost",
                                    "origin_server_ts": 1513937551203,
                                    "sender": "@example:localhost",
                                    "state_key": "",
                                    "type": "m.room.create",
                                    "unsigned": {
                                        "age": 7034220691
                                    }
                                },
                                {
                                    "content": {
                                        "aliases": [
                                            "#tutorial:localhost"
                                        ]
                                    },
                                    "event_id": "$15139375516NUgtD:localhost",
                                    "origin_server_ts": 1513937551720,
                                    "sender": "@example:localhost",
                                    "state_key": "localhost",
                                    "type": "m.room.aliases",
                                    "unsigned": {
                                        "age": 7034220174
                                    }
                                },
                                {
                                    "content": {
                                        "topic": "\ud83d\ude00"
                                    },
                                    "event_id": "$151957878228ssqrJ:localhost",
                                    "origin_server_ts": 1519578782185,
                                    "sender": "@example:localhost",
                                    "state_key": "",
                                    "type": "m.room.topic",
                                    "unsigned": {
                                        "age": 1392989709,
                                        "prev_content": {
                                            "topic": "test"
                                        },
                                        "prev_sender": "@example:localhost",
                                        "replaces_state": "$151957069225EVYKm:localhost"
                                    }
                                },
                                {
                                    "content": {
                                        "ban": 50,
                                        "events": {
                                            "m.room.avatar": 50,
                                            "m.room.canonical_alias": 50,
                                            "m.room.history_visibility": 100,
                                            "m.room.name": 50,
                                            "m.room.power_levels": 100
                                        },
                                        "events_default": 0,
                                        "invite": 0,
                                        "kick": 50,
                                        "redact": 50,
                                        "state_default": 50,
                                        "users": {
                                            "@example:localhost": 100
                                        },
                                        "users_default": 0
                                    },
                                    "event_id": "$15139375512JaHAW:localhost",
                                    "origin_server_ts": 1513937551359,
                                    "sender": "@example:localhost",
                                    "state_key": "",
                                    "type": "m.room.power_levels",
                                    "unsigned": {
                                        "age": 7034220535
                                    }
                                },
                                {
                                    "content": {
                                        "alias": "#tutorial:localhost"
                                    },
                                    "event_id": "$15139375513VdeRF:localhost",
                                    "origin_server_ts": 1513937551461,
                                    "sender": "@example:localhost",
                                    "state_key": "",
                                    "type": "m.room.canonical_alias",
                                    "unsigned": {
                                        "age": 7034220433
                                    }
                                },
                                {
                                    "content": {
                                        "avatar_url": None,
                                        "displayname": "example2",
                                        "membership": "join"
                                    },
                                    "event_id": "$152034824468gOeNB:localhost",
                                    "membership": "join",
                                    "origin_server_ts": 1520348244605,
                                    "sender": "@example2:localhost",
                                    "state_key": "@example2:localhost",
                                    "type": "m.room.member",
                                    "unsigned": {
                                        "age": 623527289,
                                        "prev_content": {
                                            "membership": "leave"
                                        },
                                        "prev_sender": "@example:localhost",
                                        "replaces_state": "$152034819067QWJxM:localhost"
                                    }
                                },
                                {
                                    "content": {
                                        "algorithm": "m.megolm.v1.aes-sha2",
                                        "rotation_period_ms": 604800000,
                                        "rotation_period_msgs": 100
                                    },
                                    "event_id": "$143273582443PhrSn:example.org",
                                    "origin_server_ts": 1432735824653,
                                    "room_id": "!jEsUZKDJdhlrceRyVU:example.org",
                                    "sender": "@example:example.org",
                                    "state_key": "",
                                    "type": "m.room.encryption",
                                    "unsigned": {
                                        "age": 1234
                                    }
                                }
                            ]
                        },
                        "timeline": {
                            "events": [
                                {
                                    "content": {
                                        "body": "baba",
                                        "format": "org.matrix.custom.html",
                                        "formatted_body": "<strong>baba</strong>",
                                        "msgtype": "m.text"
                                    },
                                    "event_id": "$152037280074GZeOm:localhost",
                                    "origin_server_ts": 1520372800469,
                                    "sender": "@example:localhost",
                                    "type": "m.room.message",
                                    "unsigned": {
                                        "age": 598971425
                                    }
                                }
                            ],
                            "limited": True,
                            "prev_batch": "t392-516_47314_0_7_1_1_1_11444_1"
                        },
                        "unread_notifications": {
                            "highlight_count": 0,
                            "notification_count": 11
                        }
                    }
                },
                "leave": {}
            },
            "to_device": {
                "events": []
            }
    }

    @property
    def keys_upload_response(self):
        return {
          "one_time_key_counts": {
              "curve25519": 10,
              "signed_curve25519": 20
          }
        }

    @property
    def keys_query_response(self):
        return {
          "device_keys": {
              "@alice:example.org": {
                  "JLAFKJWSCS": {
                      "algorithms": [
                          "m.olm.v1.curve25519-aes-sha2",
                          "m.megolm.v1.aes-sha2"
                      ],
                      "device_id": "JLAFKJWSCS",
                      "user_id": "@alice:example.org",
                      "keys": {
                          "curve25519:JLAFKJWSCS": "wjLpTLRqbqBzLs63aYaEv2Boi6cFEbbM/sSRQ2oAKk4",
                          "ed25519:JLAFKJWSCS": "nE6W2fCblxDcOFmeEtCHNl8/l8bXcu7GKyAswA4r3mM"
                      },
                      "signatures": {
                          "@alice:example.org": {
                              "ed25519:JLAFKJWSCS": "m53Wkbh2HXkc3vFApZvCrfXcX3AI51GsDHustMhKwlv3TuOJMj4wistcOTM8q2+e/Ro7rWFUb9ZfnNbwptSUBA"
                          }
                      }
                  }
              }
          },
          "failures": {}
        }

    @property
    def empty_sync(self):
        return {
            "account_data": {
                "events": []
            },
            "device_lists": {
                "changed": [],
                "left": []
            },
            "device_one_time_keys_count": {
                "signed_curve25519": 50
            },
            "groups": {
                "invite": {},
                "join": {},
                "leave": {}
            },
            "next_batch": "s1059_133339_44_763_246_1_586_12411_1",
            "presence": {
                "events": []
            },
            "rooms": {
                "invite": {},
                "join": {},
                "leave": {}
            },
            "to_device": {
                "events": []
            }
        }

    @property
    def messages_response(self):
        return {
            "chunk": [
              {
                "age": 1042,
                "content": {
                  "body": "hello world",
                  "msgtype": "m.text"
                },
                "event_id": "$1444812213350496Caaaa:example.com",
                "origin_server_ts": 1444812213737,
                "room_id": "!Xq3620DUiqCaoxq:example.com",
                "sender": "@alice:example.com",
                "type": "m.room.message"
              },
              {
                "age": 20123,
                "content": {
                  "body": "the world is big",
                  "msgtype": "m.text"
                },
                "event_id": "$1444812213350496Cbbbb:example.com",
                "origin_server_ts": 1444812194656,
                "room_id": "!Xq3620DUiqCaoxq:example.com",
                "sender": "@alice:example.com",
                "type": "m.room.message"
              },
              {
                "age": 50789,
                "content": {
                  "name": "New room name"
                },
                "event_id": "$1444812213350496Ccccc:example.com",
                "origin_server_ts": 1444812163990,
                "prev_content": {
                  "name": "Old room name"
                },
                "room_id": "!Xq3620DUiqCaoxq:example.com",
                "sender": "@alice:example.com",
                "state_key": "",
                "type": "m.room.name"
              }
            ],
            "end": "t47409-4357353_219380_26003_2265",
            "start": "t47429-4392820_219380_26003_2265"
        }

    @property
    def empty_messages(self):
        return {
            "chunk": [],
            "end": "t47429-4392820_219380_26003_2277",
            "start": "t47409-4357353_219380_26003_2265"
        }

    async def test_login(self, client):
        await client.receive_response(self.login_response)
        assert client.logged_in

    async def test_start_loop(self, client, aioresponse):
        sync_url = re.compile(
            r'^https://example\.org/_matrix/client/r0/sync\?access_token=.*'
        )

        aioresponse.get(
            sync_url,
            status=200,
            payload=self.initial_sync_response,
            repeat=True
        )

        aioresponse.post(
            "https://example.org/_matrix/client/r0/keys/upload?access_token=abc123",
            status=200,
            payload=self.keys_upload_response,
            repeat=True
        )

        aioresponse.post(
            "https://example.org/_matrix/client/r0/keys/query?access_token=abc123",
            status=200,
            payload=self.keys_query_response,
            repeat=True
        )

        await client.receive_response(self.login_response)

        # Set a big history fetch delay so it doesn't consume the fetch tasks.
        client.pan_conf.history_fetch_delay = 10
        client.start_loop(100)

        # Sync tasks are done after we get a sync event so wait for two of them
        await client.synced.wait()
        await client.synced.wait()

        # Make sure that we have only a single history fetch task for the
        # single room we have
        assert not client.history_fetch_queue.empty()
        assert client.history_fetch_queue.qsize() == 1

        # Do another round to be sure we don't get more tasks than necessary.
        await client.synced.wait()
        assert client.history_fetch_queue.qsize() == 1

        await client.loop_stop()

    async def test_history_fetching_tasks(self, client, aioresponse):
        sync_url = re.compile(
            r'^https://example\.org/_matrix/client/r0/sync\?access_token=.*'
        )

        aioresponse.get(
            sync_url,
            status=200,
            payload=self.initial_sync_response,
        )

        aioresponse.get(
            sync_url,
            status=200,
            payload=self.empty_sync,
            repeat=True
        )

        aioresponse.post(
            "https://example.org/_matrix/client/r0/keys/upload?access_token=abc123",
            status=200,
            payload=self.keys_upload_response,
            repeat=True
        )

        aioresponse.post(
            "https://example.org/_matrix/client/r0/keys/query?access_token=abc123",
            status=200,
            payload=self.keys_query_response,
            repeat=True
        )

        messages_url = re.compile(
            r'^https://example\.org/_matrix/client/r0/rooms/{}/messages\?.*'.format(TEST_ROOM_ID)
        )

        aioresponse.get(
            messages_url,
            status=200,
            payload=self.messages_response
        )

        aioresponse.get(
            messages_url,
            status=200,
            payload=self.empty_messages,
            repeat=True
        )

        await client.receive_response(self.login_response)

        client.start_loop(100)

        await client.new_fetch_task.wait()

        # Load the currently waiting task
        tasks = client.pan_store.load_fetcher_tasks(
            client.server_name,
            client.user_id
        )
        assert len(tasks) == 1

        # Check that the task is our prev_batch from the sync resposne
        assert tasks[0].room_id == TEST_ROOM_ID
        assert tasks[0].token == "t392-516_47314_0_7_1_1_1_11444_1"

        # Let's wait for the next fetch task
        await client.new_fetch_task.wait()

        tasks = client.pan_store.load_fetcher_tasks(
            client.server_name,
            client.user_id
        )
        assert len(tasks) == 1

        # Check that the task is our end token from the messages resposne
        assert tasks[0].room_id == TEST_ROOM_ID
        assert tasks[0].token == "t47409-4357353_219380_26003_2265"

        # Wait for the next fetch loop iteration.
        await client.fetch_loop_event.wait()

        tasks = client.pan_store.load_fetcher_tasks(
            client.server_name,
            client.user_id
        )
        # Check that there are no more tasks since we reached the start of the
        # room timeline.
        assert not tasks

        await client.loop_stop()
