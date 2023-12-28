from datetime   import datetime
from typing     import Any, List, Literal, Optional, Tuple, Union
from discord    import Colour, Embed
def make_embed(
        *,
        title: str = None,
        description: str = None,
        url: str = None,
        color: Union[Colour, int] = None,
        thumbnail_url: str = None,
        image_url: str = None,
        author_text: str = None,
        author_url: str = None,
        author_icon: str = None,
        footer_text: str = None,
        footer_icon: str = None,
        timestamp: Union[datetime, bool] = False,
        fields: Optional[List[Tuple[str, Any, bool]]] 
    ) -> Embed:
        """Creates and returns a Discord embed with the provided parameters.

        All parameters are optional.

        Parameters:
        -----------
        title: :class:`str`
            The embed's title.

        description: :class:`str`
            The main text body of the embed.

        url: :class:`str`
            The URL for the embed title to link to.

        color: Optional[Union[:class:`Colour`, :class:`int`]]
            The desired accent color. Defaults to :func:`colors.random_all()`

        thumbnail_url: :class:`str`
            The URL for the embed's desired thumbnail image.

        image_url: :class:`str`
            The URL for the embed's desired main image.

        footer_text: :class:`str`
            The text to display at the bottom of the embed.

        footer_icon: :class:`str`
            The icon to display to the left of the footer text.

        author_name: :class:`str`
            The text to display at the top of the embed.

        author_url: :class:`str`
            The URL for the author text to link to.

        author_icon: :class:`str`
            The icon that appears to the left of the author text.

        timestamp: Union[:class:`datetime`, `bool`]
            Whether to add the current time to the bottom of the embed.
            Defaults to ``False``.

        fields: Tuple[:class:`str`, `Any`, `bool`]
            Whether to add extra fields to the embed.
            `str`: for the name.
            `Any`: for the value.
            `Bool`: for inline. 
            Defaults to ``False``.

        Returns:
        --------
        :class:`Embed`
            The finished embed object.

        """

        embed = Embed(
            colour=color,
            title=title,
            description=description,
            url=url
        )

        embed.set_thumbnail(url=thumbnail_url)
        embed.set_image(url=image_url)

        if author_text is not "":
            embed.set_author(
                name=author_text,
                url=author_url,
                icon_url=author_icon
            )

        if footer_text is not "":
            embed.set_footer(
                text=footer_text,
                icon_url=footer_icon
            )

        if isinstance(timestamp, datetime):
            embed.timestamp = timestamp
        elif timestamp is True:
            embed.timestamp = datetime.now()

        if fields is not None:
            for field in fields:
                if len(field) == 2:
                    embed.add_field(name=field[0], value=field[1], inline=False)
                elif len(field) == 3:
                    embed.add_field(name=field[0], value=field[1], inline=field[2])

        return embed
