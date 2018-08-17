<?php

//tests/TestCase/Controller/PersonsControllerTest.php

namespace App\Test\TestCase\Controller;

use App\Controller\PersonsController;
use Cake\TestSuite\IntegrationTestCase;

/**
 * App\Controller\PersonsController Test Case
 */
class PersonsControllerTest extends IntegrationTestCase
{

    /**
     * Fixtures
     *
     * @var array
     */
    public $fixtures = [
        'app.persons'
    ];

    /**
     * Test index method
     *
     * @return void
     */
    public function testIndex()
    {
        //$this->markTestIncomplete('Not implemented yet.');
        $this->get('/persons/index');
        $this->assertResponseOk();
    }

    /**
     * Test view method
     *
     * @return void
     */
    /*
    public function testView()
    {
        //$this->markTestIncomplete('Not implemented yet.');
    }
     */

    /**
     * Test add method
     *
     * @return void
     */
    /*
    public function testAdd()
    {
        $this->markTestIncomplete('Not implemented yet.');
    }
     */

    /**
     * Test edit method
     *
     * @return void
     */
    /*
    public function testEdit()
    {
        $this->markTestIncomplete('Not implemented yet.');
    }
     */

    /**
     * Test delete method
     *
     * @return void
     */
    /*
    public function testDelete()
    {
        $this->markTestIncomplete('Not implemented yet.');
    }
     */

    public function testGetNotExistsPath()
    {
        $this->get('/persons/not_existing');

        $this->assertResponseError();
        $this->assertResponseContains('Error');
    }
}
