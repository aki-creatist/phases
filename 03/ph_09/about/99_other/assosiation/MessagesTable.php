<?php
namespace App/Model/Table;

use App/Model/Entity/Message;
use Cake/ORM/Query;
use Cake/ORM/RulesChecker;
use Cake/ORM/Table;
use Cake/Validation/Validator;

class MessagesTable extends Table
{
    public function initialize(array $config)
    {
        parent::initialize($config);

        $this->table('messages');
        $this->displayField('title');
        $this->primaryKey('id');

        $this->belongsTo('Members', [
            'foreignKey' => 'members_id',
            'joinType' => 'INNER'
        ]);
    }

    public function validationDefault(Validator $validator)
    {
        $validator
            ->add('id', 'valid', ['rule' => 'numeric'])
            ->allowEmpty('id', 'create');

        $validator
            ->requirePresence('title', 'create')
            ->notEmpty('title');

        $validator
            ->allowEmpty('comment');

        return $validator;
    }

    public function buildRules(RulesChecker $rules)
    {
        $rules->add($rules->existsIn(['members_id'], 'Members'));
        return $rules;
    }
}