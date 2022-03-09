import React from "react";

import BlockSmall from "../components/BlockSmall";

export default class BlockchainView extends React.Component {
    blocks = [
        {
            id: 1,
            txs: 15
        },
        {
            id: 2,
            txs: 15
        },
        {
            id: 3,
            txs: 15
        },
        {
            id: 4,
            txs: 15
        },
    ]
    render = () => {
        return (
            <>
                <div className="blockchain-blocks">
                    {this.blocks.map((block) => {
                        return(
                            <BlockSmall key={block.id} block={block}/>
                        )
                    })}
                </div>
            </>
        )
    }
}