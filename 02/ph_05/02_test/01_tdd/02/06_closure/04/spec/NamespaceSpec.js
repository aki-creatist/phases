var Namespace = require('../src/Namespace')

describe("ネームスペースのテスト", function () {

    it('test should create non-existent object', function () {
        Namespace.namespace('namespacetest')
        expect(typeof Namespace.namespace).toBe(typeof function(){})
    })
    it('test should not overwrite existing objects', function () {
        Namespace.nstest = { nested: {} }
        var result = Namespace.namespace("nstest.nested");
        expect(Namespace.nstest.nested).toBe(result)
    })
    it('test only create missing parts', function () {
        var existing = {}
        Namespace.nstest = { nested: {existing: existing}}
        var result = Namespace.namespace("nstest.nested.ui")
        expect(existing).toBe(Namespace.nstest.nested.existing)
        expect(typeof Namespace.nstest.nested.ui).toBe(typeof {})
    })
    it('test namespacing inside other objects', function () {
        var custom = { namespace: Namespace.namespace };
        custom.namespace("dom.event");
        expect(typeof custom.dom.event).toBe(typeof {})
        expect(typeof Namespace.dom).toBe('undefined')
    })
})
