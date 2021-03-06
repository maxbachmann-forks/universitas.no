import { connect } from 'react-redux'
import { Tool } from 'components/tool'
import { MODEL, actions, selectors } from './model.js'
import { toRoute } from 'prodsys/ducks/router'
import { parseText, renderText } from 'markup'
import { getPanes, togglePane } from 'prodsys/ducks/ux'
import ModelTools from 'components/ModelTools.js'
import OpenInDjangoAdmin from 'components/OpenInDjangoAdmin'

const openUrl = url => () => window.open(url)

let PaneTool = ({ name, active, toggle, icon, label, title }) => (
  <Tool
    {...{ icon, label, title }}
    active={active}
    onClick={() => toggle(!active)}
  />
)

PaneTool = connect(
  (state, { name }) =>
    R.pipe(
      getPanes,
      R.prop(name),
      R.objOf('active'),
    )(state),
  (dispatch, { name }) => ({
    toggle: status => dispatch(togglePane(name, status)),
  }),
)(PaneTool)

const StoryTools = ({
  trashStory,
  cloneStory,
  public_url,
  action,
  pk,
  fixStory,
}) => (
  <ModelTools>
    <Tool
      icon="Add"
      label="kopier"
      disabled={!pk}
      title={pk ? 'kopier saken' : 'velg en sak'}
      onClick={cloneStory}
      order={-1}
    />
    <PaneTool
      icon="TextFields"
      label="tekst"
      title="rediger tekst"
      name="storyText"
    />
    <PaneTool
      icon="Images"
      label="bilder"
      title="koble bilder til saken"
      name="storyImages"
    />
    <PaneTool
      icon="Eye"
      label="vis"
      title="forhåndsvisning"
      disabled={!pk}
      name="storyPreview"
    />
    <Tool
      icon="Magic"
      disabled={!pk}
      label="fiks"
      title={pk ? 'fiks tags' : 'velg en sak'}
      onClick={fixStory}
      order={-1}
    />
    <Tool
      icon="Newspaper"
      label="åpne"
      title={public_url && `se saken på universitas.no\n${public_url}`}
      onClick={public_url && openUrl(public_url)}
      disabled={!public_url}
      order={5}
    />
    <OpenInDjangoAdmin pk={pk} path="stories/story" />
  </ModelTools>
)

const mapStateToProps = (state, { pk }) =>
  R.applySpec({
    public_url: R.pipe(
      selectors.getItem(pk),
      R.prop('public_url'),
    ),
  })(state)

const mapDispatchToProps = (dispatch, { pk }) => ({
  trashStory: () =>
    dispatch(actions.fieldChanged(pk, 'publication_status', 15)),
  cloneStory: () => dispatch(actions.itemCloned(pk)),
  fixStory: () => dispatch({ type: 'FIX_STORY', payload: { pk } }),
})

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(StoryTools)
