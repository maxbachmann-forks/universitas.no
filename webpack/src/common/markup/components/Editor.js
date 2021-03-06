import { toJson } from 'utils/text'
import { parseText, renderText } from 'markup/index'
import { getScroll, setScroll } from 'utils/scroll'

import './Editor.scss'

const EditArea = ({ _ref, ...props }) => (
  <textarea
    className="EditArea"
    spellCheck={true}
    lang="nb"
    ref={_ref}
    {...props}
  />
)

const PreviewTree = ({ nodeTree, _ref, ...props }) => (
  <pre className="PreviewTree" ref={_ref} {...props}>
    {toJson(nodeTree)}
  </pre>
)

const Reverse = ({ nodeTree, _ref, ...props }) => (
  <pre className="Reverse" ref={_ref} {...props}>
    {renderText(nodeTree)}
  </pre>
)

class Editor extends React.Component {
  constructor(props) {
    super(props)
    const { value } = props
    this.state = {
      value,
      nodeTree: parseText(value),
    }
    this.changeHandler = this.changeHandler.bind(this)
    this.syncronizeScroll = this.syncronizeScroll.bind(this)
  }

  changeHandler(ev) {
    const value = ev.target.value
    this.setState({ value, nodeTree: parseText(value) })
  }

  syncronizeScroll(ev) {
    const steps = 1024
    const element = ev.currentTarget
    const scrollTop = Math.round(getScroll(element) * steps) / steps
    const refs = ['preview', 'reverse', 'tree', 'editarea']
    for (let ref of refs) {
      const refElement = this[ref]
      if (refElement != element) setScroll(refElement, scrollTop)
    }
  }

  render() {
    const { value, nodeTree } = this.state
    return (
      <div className="Editor">
        <EditArea
          value={value}
          onChange={this.changeHandler}
          onScroll={this.syncronizeScroll}
          _ref={el => (this.editarea = el)}
        />
        <Reverse
          nodeTree={nodeTree}
          onClick={this.syncronizeScroll}
          _ref={el => (this.reverse = el)}
        />
        <PreviewTree
          nodeTree={nodeTree}
          onClick={this.syncronizeScroll}
          _ref={el => (this.tree = el)}
        />
      </div>
    )
  }
}

export default Editor
