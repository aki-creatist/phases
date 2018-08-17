describe('TabTest >', function () {
    beforeEach(function () {
        var Namespace = require('../libs/main.js');
        this.tabController = Namespace.ui.tabController;
    });
    describe('TabControllerCreateTest', function () {
        it('test should fail without element', function () {
            tabController = this.tabController;
            expect(function () {
                tabController.create();
            }).toThrowError("element is not an element");
        });
        it('test should fail without element class', function () {
            tabController = this.tabController;
            expect(function () {
                tabController.create({});
            }).toThrowError("element is not an element");
        });
        it('should return object', function () {
            if (this.tabs != null) {
                var controller = this.tabController.create(this.tabs);
                expect(typeof controller).toBe(typeof {});
            }
        });
        it('test should add js-tabs class name to element', function () {
            if (this.tabs != null) {
                var tabs = this.tabController.create(this.tabs);
                expect(this.tabs.classList.contains("js-tab-controller")).toBeTruthy();
            }
        });
    });
    describe('TabbedControllerActivateTabTest', function () {
        beforeEach(function () {
            document.body.innerHTML = window.__html__['spec/index.html'];
            this.tabs = document.getElementById("tabs");
            if (this.tabs != null) {
                this.controller = this.tabController.create(this.tabs);
                this.links = this.tabs.getElementsByTagName("a");
                this.lis = this.tabs.getElementsByTagName("li");
            } else {
                console.log('this.tabs is empty');
            }
        });
        it('test should not fail without anchor', function () {
            expect(this.controller.activateTab).not.toThrow();
        });
        it('test should mark anchor as active', function () {
            this.controller.activateTab(this.links[0]); //クラスの追加
            expect(this.links[0].classList.contains("active-tab")).toBeTruthy();
        });
        it('test should deactivate previous tab', function () {
            this.controller.activateTab(this.links[0]);
            this.controller.activateTab(this.links[1]);
            expect(this.links[0]).not.toMatch(/(^|\s)active-tab(\s|$)/);
            expect(this.links[1].classList.contains("active-tab")).toBeTruthy();
        });
        it('test should not activate unsupported element types', function () {
            this.controller.activateTab(this.links[0]);
            this.controller.activateTab(this.lis[0]);
            expect(this.lis[0]).not.toMatch(/(^|\s)active-tab(\s|$)/);
            expect(this.links[0].classList.contains("active-tab")).toBeTruthy();
        });
        it('test should fire onTabChange', function () {
            var actualPrevious, actualCurrent;
            this.controller.activateTab(this.links[0]);
            this.controller.onTabChange = function (curr, prev) {
                actualPrevious = prev;
                actualCurrent = curr;
            };
            this.controller.activateTab(this.links[1]);
            expect(actualPrevious).toBe(this.links(0));
            expect(actualCurrent).toBe(this.links(1));
        })
    });
});