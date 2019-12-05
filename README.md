# thethe

Site: [https://thethe.e-paths.com](https://thethe.e-paths.com/)

## Install (development enviroment)

- git clone ...
- Create a Python virtual enviroment, activate it and pip -r requirements.txt
- docker-compose build
- cd frontend and npm install

## Running (development enviroment)

In a Python virtual enviroment activated (you can choose to run them in background or in separate panes):

```bash
watchmedo auto-restart -d tasks -p '*.py' -- celery -A tasks.tasks:celery_app worker -l info
```

```bash
gunicorn server.main:app --reload
```

Frontend:

```bash
cd frontend
npm run dev
```

### A complete docker image is scheduled to be released soon

## Problems with Celery

---

### Celery + Python 3.7

Install Celery from github:

pip install https://github.com/celery/celery

## Adding the initial account

---

Create a collection (Mongodb) called "thethe".
Create a document "users" with an entry:

{username: "yourusername", password: "hash"}

hash is (assuming python env is activated and requirements.txt are installed) gotten from a python interactive interpreter:

```python
from passlib.apps import custom_app_context as pwd_context
pwd_context.encrypt("yourpassword")
```

Copy the hash into the value of password field. Done.

## How to create a plugin for THETHE

Plugins affect one or more resources. It may have a frontend counterpart written as a Vue (javascript) component. Plugins must registers itself to describe what they do, etc.

When the plugin is launched it may be queued in a Celery queue for background processing (or not, depending in the kind of tasks, actions, etc.)

A plugin does have the following structure:

### Python plugin

---

A plugin in Python is just for describe the actions, description, name, category, etc. It must inherit from **plugin_base/Plugin**

The plugin **MUST** be located in **server/plugins/** folder. Below is an exrtract of **server/plugins/geoip.py**

```python
RESOURCE_TARGET = [ResourceType.IPv4]

# Plugin Metadata {a decription, if target is actively reached and name}
PLUGIN_DESCRIPTION = "Use a GeoIP service to geolocate an IP address"
PLUGIN_IS_ACTIVE = False
PLUGIN_NAME = "geoip"


class Plugin:
    description = PLUGIN_DESCRIPTION
    is_active = PLUGIN_IS_ACTIVE
    name = PLUGIN_NAME

    def __init__(self, resource, project_id):
        self.project_id = project_id
        self.resource = resource

    def do(self):
        resource_type = self.resource.get_type()

        try:
            to_task = {
                "ip": self.resource.get_data()["address"],
                "resource_id": self.resource.get_id_as_string(),
                "project_id": self.project_id,
                "resource_type": resource_type.value,
                "plugin_name": Plugin.name,
            }
            geoip_task.delay(**to_task)

        except Exception as e:
            tb1 = traceback.TracebackException.from_exception(e)
            print("".join(tb1.format()))

```

### Celery task

---

Finally, the task is introduced as a Celery function which gives us async results. It **SHOULD** be located into **tasks/tasks.py** file with the proper Celery decorators

```python
@celery_app.task
def geoip_task(plugin_name, project_id, resource_id, resource_type, ip):
    try:
        query_result = geoip(ip)
        if not query_result:
            return

        # TODO: See if ResourceType.__str__ can be use for serialization
        resource_type = ResourceType(resource_type)
        resource = Resources.get(resource_id, resource_type)
        resource.set_plugin_results(
            plugin_name, project_id, resource_id, resource_type, query_result
        )

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
```

### Celery subtask

---

You **MAY** split the core functionality in a external module located into the **tasks/subtasks** folder.

```python
def geoip(ip):
    try:
        URL = f"http://api.ipstack.com/{ip}?access_key={API_KEY}&format=1"
        response = urllib.request.urlopen(URL).read()
        return json.loads(response)

    except Exception as e:
        tb1 = traceback.TracebackException.from_exception(e)
        print("".join(tb1.format()))
        return None
```

### Vue component

---

Finally, the frontend **MIGHT** know hot to represent the results as a view. As the system is designed to support dynamic load of plugins all the Vue components are loaded under demand via the **DynamicComponent** component.

Plugins must have an entry into the **frontend/src/components/templates/\<plugin name\>/index.vue**

Here you must deal with the plugins results presentation. As an example (taking GeoIp plugin):

```javascript
<template>
  <v-layout row pt-2 wrap class="subheading">
    <v-flex lg5>
      <v-flex>
        <v-card>
          <v-card-title primary-title>
            <span class="subheading">Geolocalization</span>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <v-layout row>
              <v-flex lg-6 class="text-xs-left">
                <v-layout column>
                  <v-flex>
                    <v-label>Continent:</v-label>
                  </v-flex>
                  <v-flex>
                    <v-label>Country:</v-label>
                  </v-flex>
                  <v-flex>
                    <v-label>Region:</v-label>
                  </v-flex>
                  <v-flex>
                    <v-label>City:</v-label>
                  </v-flex>
                  <v-flex>
                    <v-label>Zip:</v-label>
                  </v-flex>
                  <v-flex>
                    <v-label>Latitude:</v-label>
                  </v-flex>
                  <v-flex>
                    <v-label>Longitude:</v-label>
                  </v-flex>
                  <v-flex v-if="resource.country_code">
                    <v-label>Flag:</v-label>
                  </v-flex>
                </v-layout>
              </v-flex>
              <v-flex lg-6 class="text-xs-right">
                <v-layout column>
                  <v-flex>{{ resource.continent_name }}</v-flex>
                  <v-flex>{{ resource.country_name }}</v-flex>
                  <v-flex>{{ resource.region_name }}</v-flex>
                  <v-flex>{{ resource.city }}</v-flex>
                  <v-flex>{{ resource.zip }}</v-flex>
                  <v-flex>{{ resource.latitude }}</v-flex>
                  <v-flex>{{ resource.longitude }}</v-flex>
                  <v-flex v-if="resource.country_code">
                    <country-flag :country="resource.country_code"></country-flag>
                  </v-flex>
                </v-layout>
              </v-flex>
            </v-layout>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-flex>
  </v-layout>
</template>

<script>
import { make_unique_list } from "../../../utils/utils";

export default {
  name: "geoip",
  props: {
    plugin_results: Object
  },
  data: function() {
    return {};
  },
  computed: {
    resource: function() {
      let plugin_result = { ...this.plugin_results };
      return plugin_result;
    }
  }
};
</script>
```
