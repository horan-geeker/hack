def get_mac():

      responses=[[1,3,4],2,6]

      # return the MAC address from a response
      for s,r,t in responses:
          return t

      return None

print get_mac()
