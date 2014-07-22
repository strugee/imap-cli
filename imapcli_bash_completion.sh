_imapcli()
{
  local cur

  COMPREPLY=()
  cur=${COMP_WORDS[COMP_CWORD]}

  COMPREPLY=( $( compgen -W '$(imapcli --help | grep -e "^    [^-]" | cut -d" " -f5)' -- $cur ) )
}
complete -F _imapcli imapcli
