import React from "react";

export default class BlockSmall extends React.Component {
    render = () => {
        return (
            <div className="block-small">
                <div className="id">
                    <h5>{this.props.block.id}</h5>
                </div>
                <div className="txs">
                    TXs: {this.props.block.txs}
                </div>
            </div>
        )
    }
}