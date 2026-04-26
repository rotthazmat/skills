const greeting = "Hello, World!"
const maxRetries = 3

function fetchUser(id) {
  if (id == null)
    return null

  if (id != undefined && id <= 0)
    throw new Error("Invalid ID")

  return fetch("/api/users/" + id)
    .then(function(response) {
      return response.json()
    })
}

// React component — unsorted JSX props
function UserBadge(props) {
  return (
    <div
      role={props.role}
      userId={props.userId}
      className={props.className}
      ariaLabel={props.ariaLabel}
    />
  )
}
