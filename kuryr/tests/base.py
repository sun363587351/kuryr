# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from neutronclient.tests.unit.test_cli20 import CLITestV20Base

from kuryr import app


class TestCase(CLITestV20Base):
    """Test case base class for all unit tests."""

    def setUp(self):
        super(TestCase, self).setUp()
        app.config['DEBUG'] = True
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.app.neutron = self.client


class TestKuryrBase(TestCase):
    """Base class for all Kuryr unittests."""

    def setUp(self):
        super(TestKuryrBase, self).setUp()
        self.app.neutron.format = 'json'
        self.addCleanup(self.mox.VerifyAll)
        self.addCleanup(self.mox.UnsetStubs)

    def _mock_out_network(self, neutron_network_id, docker_network_id):
        fake_list_response = {
            "networks": [{
                "status": "ACTIVE",
                "subnets": [],
                "name": docker_network_id,
                "admin_state_up": True,
                "tenant_id": "9bacb3c5d39d41a79512987f338cf177",
                "router:external": False,
                "segments": [],
                "shared": False,
                "id": neutron_network_id
            }]
        }
        self.mox.StubOutWithMock(app.neutron, 'list_networks')
        app.neutron.list_networks(
            name=docker_network_id).AndReturn(fake_list_response)
        self.mox.ReplayAll()

        return neutron_network_id


class TestKuryrFailures(TestKuryrBase):
    """Unitests for checking if Kuryr handles the failures appropriately."""
