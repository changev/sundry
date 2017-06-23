
        it('Should create enclosure node and update when no match found', function() {
            var node = {
                id: nodeId,
                relations: []
            };
            var enclInput = {
                name: 'Enclosure Node ABC123',
                type: 'enclosure',
                relations: []
            };
            var enclOutput = _.cloneDeep(enclInput);
            var enclId = uuid.v4();

            enclOutput.relations = [{
                relationType: 'encloses',
                targets: [nodeId]
            }];

            var nodeOutput = _.cloneDeep(node);
            nodeOutput.relations = [{
                relationType: 'enclosedBy',
                targets: [enclId]
            }];

            enclOutput.id = enclId;

            var enclQuery = { name: enclInput.name, type: enclInput.type }
            this.sandbox.stub(mockWaterline.nodes,'find').resolves();
            this.sandbox.stub(mockWaterline.nodes,'findOrCreate').resolves(enclOutput);
            this.sandbox.stub(mockWaterline.nodes,'updateFieldIfNotExistByIdentifier');
            this.sandbox.stub(mockWaterline.nodes,'addListItemsIfNotExistByIdentifier');
            mockWaterline.nodes.updateFieldIfNotExistByIdentifier
            .withArgs(enclId).resolves(enclOutput);
            mockWaterline.nodes.addListItemsIfNotExistByIdentifier
            .withArgs(enclId).resolves(enclOutput);
            mockWaterline.nodes.updateFieldIfNotExistByIdentifier
            .withArgs(nodeId).resolves(nodeOutput);
            mockWaterline.nodes.addListItemsIfNotExistByIdentifier
            .withArgs(nodeId).resolves(nodeOutput);
            this.sandbox.stub(mockWaterline.nodes,'findByIdentifier').resolves(node);

            return job.run()
            .then(function() {
                expect(mockWaterline.nodes.findOrCreate)
                .to.have.been.calledWith(enclQuery, enclInput);
                expect(mockWaterline.nodes.updateFieldIfNotExistByIdentifier)
                .to.have.been.calledTwice;
                expect(mockWaterline.nodes.updateFieldIfNotExistByIdentifier)
                .to.have.been.calledWith(nodeId, "relations", []);
                expect(mockWaterline.nodes.updateFieldIfNotExistByIdentifier)
                .to.have.been.calledWith(enclId, "relations", []);
                expect(mockWaterline.nodes.addListItemsIfNotExistByIdentifier)
                .to.have.been.calledFourth;
                expect(mockWaterline.nodes.addListItemsIfNotExistByIdentifier)
                .to.have.been.calledWith(
                    enclId, 
                    {relations: [{relationType: 'encloses', targets: []}]},
                    {relationType: 'encloses'}
                );
                expect(mockWaterline.nodes.addListItemsIfNotExistByIdentifier)
                .to.have.been.calledWith(
                    enclId, 
                    {"relations.0.targets": [nodeId]}
                );
                expect(mockWaterline.nodes.addListItemsIfNotExistByIdentifier)
                .to.have.been.calledWith(
                    nodeId, 
                    {relations: [{relationType: 'enclosedBy', targets: []}]},
                    {relationType: 'enclosedBy'}
                );
                expect(mockWaterline.nodes.addListItemsIfNotExistByIdentifier)
                .to.have.been.calledWith(
                    nodeId, 
                    {"relations.0.targets": [enclId]}
                );
            });
        });