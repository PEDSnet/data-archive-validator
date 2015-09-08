import requests


class Model(object):

    # This is an awkward bit of metadata that is DCC- and time-specific
    REQUIRED_TABLES = {
        'pedsnet': [
            'entity',
            'care_site',
            'condition_occurrence',
            'death',
            'drug_exposure',
            'location',
            'measurement',
            'observation',
            'observation_period',
            'person',
            'procedure_occurrence',
            'provider',
            'visit_occurrence',
            'visit_payer',
        ],
        'i2b2': [
            'i2b2',
            'observation_fact',
            'visit_dimension',
            'patient_dimension',
            'provider_dimension',
            'concept_dimension'
        ]
    }

    def __init__(self, name, version):

        tpl = ('http://data-models.origins.link/models/'
               '{name}/{version}?format=json')
        url = tpl.format(name=name, version=version)
        try:
            r = requests.get(url)
        except requests.exceptions.ConnectionError:
            raise Exception('Network connection error accessing {0}'.format(
                url))
        if r.status_code == 404:
            raise ValueError('Invalid name or version (URL {})'.format(url))
        cdm = r.json()
        self._name = name
        self._version = version
        self._tables = dict()
        for table in cdm['tables']:
            table_name = table['name']
            if table_name not in self._tables:
                self._tables[table_name] = set()
            for field in table['fields']:
                self._tables[table_name].add(field['name'])
        
    def required_tables(self):
        return sorted(Model.REQUIRED_TABLES[self._name])

    def name(self):
        return self._name

    def version(self):
        return self._version

    def tables(self):
        return sorted(self._tables.keys())

    def fields(self, table):
        if table in self._tables:
            return sorted(self._tables[table])
        tpl = 'Table {t} not part of model {m}, version {v}'
        raise ValueError(tpl.format(t=table, m=self._name, v=self._version))
