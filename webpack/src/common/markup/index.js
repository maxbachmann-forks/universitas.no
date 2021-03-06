import rules from './rules'
import { cleanText, hashText } from 'utils/text'
export { rules }

export const makeParser = ({
  type,
  pattern,
  groups = ['content'],
  inline,
  process = R.identity,
}) => {
  const flags = R.uniq(pattern.flags + (inline ? 'y' : 'my')).join('')
  const regex = new RegExp(pattern, flags)
  return text => {
    regex.lastIndex = 0
    const result = regex.exec(text)
    if (!result) return null
    const [content, ...rest] = result
    const groupmatches = R.zipObj(groups, rest)
    return process({
      match: result,
      content,
      index: regex.lastIndex,
      type,
      ...groupmatches,
    })
  }
}

const [inlineRules, blockRules] = R.pipe(
  R.map(tag => ({ parse: makeParser(tag), ...tag })),
  R.values,
  R.sortBy(R.prop('order')),
  R.partition(R.prop('inline')),
)(rules)

// Parse markup text to render tree
// :: string -> [{nodes}]
export const parseText = (text, multiline = true, lastIndex = 0) => {
  const nodes = []
  const rules = multiline ? blockRules : inlineRules
  const types = R.pipe(
    R.pluck('type'),
    R.join(' '),
  )(rules)
  // Hack to break potential infinite loops. If theres some bug in the rules,
  // this should cause to test to fail fast, instead of running forever.
  let looplimit = 99999
  let key = 0
  while (looplimit-- && text) {
    for (const rule of rules) {
      const result = rule.parse(text)
      if (result) {
        const { index, content, ...node } = result
        if (rule.type != 'whitespace') {
          if (R.contains(rule.type, ['text', 'character'])) nodes.push(content)
          else {
            const children = rule.leaf
              ? content
                ? [content]
                : []
              : parseText(content, R.contains('\n', content))
            // node.hash = hashText(match)
            nodes.push({ ...node, children, key: key++ })
          }
        }
        // lastIndex += index
        text = text.slice(index)
        break
      }
    }
  }
  if (looplimit < 1) {
    // this should never happen. :)
    // but if it does, throw an error, which will be captured by sentry
    throw new Error(`loop limit reached for "${text}"`)
  }
  return nodes
}

// Render parse tree to markup text
// :: [{nodes}] -> string
export const renderText = tree => {
  const text = []
  for (const node of tree) {
    if (R.is(String, node)) {
      text.push(node)
    } else {
      const rule = rules[node.type]
      text.push(rule.reverse({ ...node, content: renderText(node.children) }))
      if (!rule.inline) text.push('\n')
    }
  }
  return R.pipe(
    R.join(''),
    cleanText,
    R.trim,
  )(text)
}
