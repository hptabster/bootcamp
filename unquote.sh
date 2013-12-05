unquote()
{
  echo $1 | sed -e "s.\".\\\\\".g;s.'.\&quot;.g"
}
